# Generated by Django 3.2.13 on 2022-05-17 16:46

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('conform_phone', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('solde', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('professionnel', models.BooleanField(default=False)),
                ('business', models.BooleanField(default=False)),
                ('room', autoslug.fields.AutoSlugField(editable=False, populate_from=user.models.random_string_generator, unique=True)),
                ('group', autoslug.fields.AutoSlugField(editable=False, populate_from=user.models.random_string_generator, unique=True)),
                ('channel', autoslug.fields.AutoSlugField(editable=False, populate_from=user.models.random_string_generator, unique=True)),
                ('nature_document', models.CharField(default='pas de document', max_length=255)),
                ('numero_document', models.CharField(default='0', max_length=255)),
                ('document_verif', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff_simple', models.BooleanField(default=False)),
                ('is_staff_bureau', models.BooleanField(default=False)),
                ('is_staff_comptable', models.BooleanField(default=False)),
                ('is_staff_manager', models.BooleanField(default=False)),
                ('is_staff_techique', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PayementGaalgui',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('livraison', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('relever', models.BooleanField(default=False)),
                ('annuler', models.BooleanField(default=False)),
                ('prix', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('code', models.PositiveIntegerField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViaCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True)),
                ('Nom_complet_du_receveur', models.CharField(max_length=255)),
                ('Nom_complet_de_l_envoyeur', models.CharField(blank=True, max_length=255, null=True)),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('active', models.BooleanField(default=False)),
                ('retirer', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone_beneficiaire', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('relever', models.BooleanField(default=False)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.employe')),
            ],
        ),
        migrations.CreateModel(
            name='VerificationTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_destinataire', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('nom_complet_destinataire', models.CharField(blank=True, max_length=255, null=True)),
                ('nom_complet_client', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=19)),
                ('nature_transaction', models.CharField(blank=True, choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande'), ('activation compte', 'activation compte'), ('reception payement', 'reception payement')], max_length=255)),
                ('reste', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('commission_incluse', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('code', models.PositiveIntegerField(default=0)),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.employe')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RetraitGaalguiShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=19)),
                ('relever', models.BooleanField(default=False)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.employe')),
                ('payement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.payementgaalgui')),
            ],
        ),
        migrations.CreateModel(
            name='RetraitCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiaire', models.CharField(max_length=255)),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('relever', models.BooleanField(default=False)),
                ('code', models.PositiveIntegerField()),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Retrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('relever', models.BooleanField(default=False)),
                ('beneficiaire', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=100)),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.pays')),
            ],
        ),
        migrations.CreateModel(
            name='PointAcces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=255)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.region')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneVerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nature_transaction', models.CharField(choices=[('envoi direct', 'envoi direct'), ('envoi via code', 'envoi via code'), ('depot', 'depot'), ('retrait', 'retrait'), ('reception', 'reception'), ('payement', 'payement'), ('code', 'code'), ('retrait par code', 'retrait par code'), ('annulation commande', 'annulation commande'), ('activation compte', 'activation compte'), ('reception payement', 'reception payement')], max_length=100)),
                ('montant', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('beneficiaire', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.PositiveIntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('donnateur', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, upload_to='static/media')),
                ('should_notify', models.BooleanField(default=False)),
                ('is_trans', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Envoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_receveur', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('relever', models.BooleanField(default=False)),
                ('envoyeur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employe',
            name='point_acces',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.pointacces'),
        ),
        migrations.AddField(
            model_name='employe',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('somme', models.DecimalField(decimal_places=2, max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('relever', models.BooleanField(default=False)),
                ('depositaire', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employe')),
            ],
        ),
        migrations.CreateModel(
            name='AnnulationGaalguiShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relever', models.BooleanField(default=False)),
                ('payement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.payementgaalgui')),
            ],
        ),
    ]
