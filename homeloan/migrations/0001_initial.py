# Generated by Django 3.1.1 on 2022-03-26 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ApplicationNumber', models.IntegerField(null=True)),
                ('PanNumber', models.CharField(max_length=50, null=True)),
                ('PanCardCopy', models.FileField(max_length=200, null=True, upload_to='')),
                ('Address', models.CharField(max_length=250, null=True)),
                ('AddressProofType', models.CharField(max_length=200, null=True)),
                ('AddressDoc', models.FileField(max_length=200, null=True, upload_to='')),
                ('ServiceType', models.CharField(max_length=250, null=True)),
                ('MontlyIncome', models.CharField(max_length=250, null=True)),
                ('ExistingLoan', models.CharField(max_length=250, null=True)),
                ('ExpectedLoanAmount', models.CharField(max_length=250, null=True)),
                ('ProfilePic', models.FileField(max_length=200, null=True, upload_to='')),
                ('Tenure', models.CharField(max_length=250, null=True)),
                ('GName', models.CharField(max_length=250, null=True)),
                ('Gmobnum', models.CharField(max_length=250, null=True)),
                ('Gemail', models.CharField(max_length=250, null=True)),
                ('Gaddress', models.CharField(max_length=250, null=True)),
                ('SubmitDate', models.DateField(null=True)),
                ('Remark', models.CharField(max_length=250, null=True)),
                ('Status', models.CharField(max_length=250, null=True)),
                ('LoanamountDisbursed', models.CharField(max_length=250, null=True)),
                ('RateofInterest', models.CharField(max_length=250, null=True)),
                ('DTenure', models.CharField(max_length=250, null=True)),
                ('UpdationDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('emailid', models.CharField(max_length=50, null=True)),
                ('contact', models.CharField(max_length=15, null=True)),
                ('message', models.CharField(max_length=300, null=True)),
                ('enquiryDate', models.DateField(null=True)),
                ('isread', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MobileNumber', models.CharField(max_length=15, null=True)),
                ('RegDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Applicationtracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Remark', models.CharField(max_length=250, null=True)),
                ('Status', models.CharField(max_length=250, null=True)),
                ('UpdationDate', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeloan.application')),
            ],
        ),
    ]
