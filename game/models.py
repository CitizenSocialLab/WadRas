from django.db import models


class AdminUser(models.Model):
    email = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300) # guardar md5

class Game(models.Model):
    name = models.CharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)

class Partida(models.Model):
    num_partida = models.IntegerField()
    estat = models.CharField(max_length=20, default="INACTIVA") # INACTIVA, REGISTRANT, COMPLETA, ENJOC, ACABADA
    classe = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides
    usuaris_registrats = models.IntegerField(default=0)
    data_creacio = models.DateTimeField()
    data_inicialitzacio = models.DateTimeField(null=True)
    data_finalitzacio = models.DateTimeField(null=True)
    comentari = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):

    # Enquesta inicial
    nickname = models.CharField(max_length=100, default="")
    on_vius = models.CharField(max_length=6, default="")
    genere = models.CharField(max_length=1, default="")
    rang_edat = models.CharField(max_length=100, default="")
    check1 = models.BooleanField(default=False)

    ####################

    num_jugador = models.IntegerField(null=True)

    status = models.CharField(max_length=100, default="")
    session_game = models.CharField(max_length=100, default="")

    # Partides
    game1 = models.ForeignKey(Partida, null=True, related_name='standard')
    game2 = models.ForeignKey(Partida, null=True, related_name='interact')
    game3 = models.ForeignKey(Partida, null=True, related_name='voive')
    game4 = models.ForeignKey(Partida, null=True, related_name='wall')

    # partida actual que esta jugant
    partida_current =  models.ForeignKey(Partida, null=True, related_name='current')

    #Variables diners
    money_game1 = models.FloatField(default=0)
    money_game2 = models.FloatField(default=0)
    money_game4 = models.FloatField(default=0)
    money_game3 = models.FloatField(default=0)

    punts_totals = models.FloatField(default=0)
    guany_final = models.IntegerField(default=0)

    is_robot = models.BooleanField(default=False)
    num_seleccions = models.IntegerField(default=0)
    acabat = models.BooleanField(default=False)

    # Data creacio user
    data_creacio = models.DateTimeField()

    # Registre
    date_register_game1 = models.DateTimeField(null=True)
    date_register_game2 = models.DateTimeField(null=True)
    date_register_game3 = models.DateTimeField(null=True)
    date_register_game4 = models.DateTimeField(null=True)

    # Finalitzacio
    date_end_game1 = models.DateTimeField(null=True)
    date_end_game2 = models.DateTimeField(null=True)
    date_end_game3 = models.DateTimeField(null=True)
    date_end_game4 = models.DateTimeField(null=True)



    updated_at = models.DateTimeField(auto_now=True)


class Resident(models.Model):

    original_id = models.IntegerField(default=0)
    nickname = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    selection = models.CharField(max_length=1, default="")
    last_selected = models.DateTimeField(null=True)


class Prisoner(models.Model):
    user = models.ForeignKey(User)
    is_robot1 = models.BooleanField(default=True)
    rol1 = models.CharField(max_length=100, default="") # ADVANTAGE OR DISVANTAGE

    partida = models.ForeignKey(Partida, null=True)

    rival1 = models.ForeignKey(User,null=True,blank=True,related_name='rival_prisoner1')
    rival1_resident = models.ForeignKey(Resident,null=True,blank=True,related_name='rival_resident1')

    guess1 = models.CharField(max_length=1, default="")
    seleccio1 = models.CharField(max_length=1, default="")

    gain1 = models.FloatField(default=0)

    data_guess1 = models.DateTimeField(null=True)
    data_seleccio1 = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)






