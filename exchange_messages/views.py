from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render

from authentication.models import UsersManager
from seeds.models import SeedManager
from trocgraines_config.settings.common import DEFAULT_FROM_EMAIL

from .forms import NewMessageForm
from .models import ExchangeMessageManager
from .text_constants import (GLOBAL_ERROR_MSG, MESSAGE_SENT,
                             MESSAGE_SENT_BUT_SAVING_ERROR,
                             NEW_EXCHANGE_MESSAGE_FOOTER,
                             NEW_EXCHANGE_MESSAGE_HEADER,
                             NEW_EXCHANGE_MESSAGE_NO_SEED_TO_EXCHANGE,
                             NEW_EXCHANGE_MESSAGE_SEED_NOT_AVAILABLE,
                             NEW_EXCHANGE_MESSAGE_SUBJECT,
                             NEW_EXCHANGE_MESSAGE_USER_MESSAGE,
                             UNABLE_TO_SEND_MESSAGE)

user_manager = UsersManager()
seed_manager = SeedManager()
exchange_message_manager = ExchangeMessageManager()


@login_required()
def new_message(request, seed_id, owner_id):
    """ prepare the message and send it """

    seed_owner = user_manager.get_user(owner_id)
    needed_seed = seed_manager.get_seed(seed_id)
    proposed_seeds_list = seed_manager.get_user_seeds(request.user.id)
    list_of_proposed_seeds = NEW_EXCHANGE_MESSAGE_NO_SEED_TO_EXCHANGE

    """ create list of user seeds """
    if proposed_seeds_list:
        list_of_seed_names = []
        for seed in proposed_seeds_list:
            if seed.available is not True:
                list_of_seed_names.append(
                    NEW_EXCHANGE_MESSAGE_SEED_NOT_AVAILABLE.format(seed.name)
                )
            else:
                list_of_seed_names.append(seed.name)
        list_of_proposed_seeds = ', \n    - '.join(list_of_seed_names)

    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            """ build the full message """
            exchange_message_data = {
                'recipient': seed_owner,
                'sender': request.user,
                'subject': NEW_EXCHANGE_MESSAGE_SUBJECT.format(
                    seed_owner.username, request.user.username
                ),
                'message': form.cleaned_data.get('message'),
            }
            """ send email to the seed owner """
            send_mail_return = 0
            try:
                send_mail_return = send_mail(
                    # email subject
                    exchange_message_data['subject'],
                    # email body
                    exchange_message_data['subject']
                    + NEW_EXCHANGE_MESSAGE_HEADER
                    + (('_' * 50) + '\n')
                    + exchange_message_data['message']
                    + ('\n' + ('_' * 50) + '\n')
                    + NEW_EXCHANGE_MESSAGE_FOOTER.format(
                        request.user.username, request.user.email
                    ),
                    # from email
                    DEFAULT_FROM_EMAIL,
                    # to email
                    [exchange_message_data['recipient'].email],
                    # raise an SMTPException if an error occurs
                    fail_silently=False,
                )
            except SMTPException as smtp_error:
                messages.error(
                    request, UNABLE_TO_SEND_MESSAGE.format(smtp_error)
                )

            if send_mail_return == 1:
                """add success message."""
                messages.success(
                    request, MESSAGE_SENT.format(request.user.username)
                )
                """ save discussion in database """
                if not exchange_message_manager.save_exchange_message(
                    **exchange_message_data
                ):

                    """add error message."""
                    messages.error(request, MESSAGE_SENT_BUT_SAVING_ERROR)
                my_discussions = exchange_message_manager.get_user_discussions(
                    request.user
                )
                context = {'my_discussions': my_discussions}
                return render(request, 'my_messages.html', context)

    new_message = NEW_EXCHANGE_MESSAGE_USER_MESSAGE.format(
        seed_owner.username, needed_seed.name, list_of_proposed_seeds
    )
    new_message_form = NewMessageForm(initial={'message': new_message})
    context = {'new_message_form': new_message_form}
    return render(request, 'new_message.html', context)


@login_required()
def my_messages(request):
    """ display / delete user messages """

    exchange_message_manager_message = []

    if request.method == 'POST':
        try:
            discussion_id = request.POST.get('delete_discussion')
            exchange_message_manager_message = (
                exchange_message_manager.delete_discussion(discussion_id)
            )
        except Http404:
            exchange_message_manager_message.append({40: GLOBAL_ERROR_MSG})

    if exchange_message_manager_message:
        for message in exchange_message_manager_message:
            for level, content in message.items():
                messages.add_message(request, level, content)

    my_discussions = exchange_message_manager.get_user_discussions(
        request.user
    )
    context = {'my_discussions': my_discussions}
    return render(request, 'my_messages.html', context)
