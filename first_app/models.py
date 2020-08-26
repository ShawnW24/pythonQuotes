from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def loginValidator(self, postData):
        errors = {}
        usersWithEmail= User.objects.filter(email=postData['form_email'])
        if len(usersWithEmail) == 0:
            errors['emailreq']= "Email is Required!"
        elif len(usersWithEmail) == 0:
            errors['emailnotFound']= "Email not Found, Please Register!"
        else:
            userToCheck= usersWithEmail[0]
            if bcrypt.checkpw(postData['form_pw'].encode(),usersWithEmail[0].password.encode()):
                print("password matches")
            else:
                errors['pwmatch']= "Password is Inncorrect!"
        return errors

    def reqValidator(self,postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['form_fname']) < 2:
            errors['fnamereq']="First Name Required with at least 2 Characters"
        if len(postData['form_lname']) < 2:
            errors['lnamereq']="Last Name Required with at least 2 Characters"
        if len(postData['form_email'])==0:
            errors['emailreq']="Email Required"
        elif not EMAIL_REGEX.match(postData['form_email']):
            errors['invalidEmail']="Email Not Real"
        else:
            repeatEmail=User.objects.filter(email=postData['form_email'])
            if len(repeatEmail) > 0:
                errors['emailTaken']= "Email Already Taken!"
        if len(postData['form_pw'])< 8:
            errors['pwreq']="Password Must Be At Least 8 Characters "
        if postData['form_pw']!= postData['form_cpw']:
            errors['confirmpw']="Passwords Must Match!"
        return errors

class QuoteManager(models.Manager):
    def quoteValidator(self,postData):
        errors={}
        if len(postData['form_author']) < 2:
            errors['authorlength'] = "Author must be at least 2 Characters"
        if len(postData['form_quote']) < 10:
            errors['quotelength']="Quote Must Be at least 5 Characters"
        return errors

class User(models.Model):
    firstName=models.CharField(max_length=255)
    lastName=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Quote(models.Model):
    content=models.TextField()
    author=models.CharField(max_length=255)
    uploader=models.ForeignKey(User, related_name="quotes_uploaded", on_delete=models.CASCADE)
    likes=models.ManyToManyField(User, related_name="quotes_liked")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=QuoteManager()