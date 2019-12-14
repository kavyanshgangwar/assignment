from django.dispatch import Signal

# created the updatesignal 
UpdateSignal = Signal(providing_args=['olderModel','changedArguments'])