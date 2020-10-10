from __future__  import print_function
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.conf import Settings
from django.utils import timezone

restriction_types = (
    ('Morgage','Morgage'),
    ('Courtorder','Court Order'),
    ('Caveat','Caveat'),
    ('Landuse','Land Use Restriction'),
)

landuse_zoning_types = (
    ('Agricultural','Agricultural'),
    ('Courtorder','Court Order'),
    ('Caveat','Caveat'),
    ('Landuse','Land Use Restriction'),
)
landcover_types = (
    ('1','Agricultural'),
    ('2','Residential'),
    ('3','Commercial'),
    ('4','Industry'),
    ('5','Public'),
    ('6','Reserve'),
)
transaction_types = (
    ('Transfer','Transfer'),
    ('Subdivision','Subdivision'),
    ('Change of user','Change of user'),
    ('Development Aplication','Development Application'),
    ('Registration','Registration'),
    ('Valuation','Valuation'),
)

status_types = (
    ('Approved','Approved'),
    ('Rejected','Rejected'),
    ('Registered','Registered'),
    ('Deleted','Deleted'),
    ('Pending','Pending'),
    ('Withdrawn','Withdrawn'),
    ('Superceeded','Superceeded'),
)

application_status = (
    ('Unverified','Unverified'),
    ('Verified','Verified'),
    ('Approved','Approved'),
    ('Completed','Completed'),
    ('Closed','Closed'),
)


party_types = (
    ('Individual','Individual'),
    ('Company','Company'),
    ('Community','Community'),
    ('Trust','Trust'),
    ('Family','Family'),
    ('Government','Government'),

)

agent_types = (
    ('Owner','Owner'),
    ('Buyer','Buyer'),
    ('Other','Other'),
)

actual_landuses = (
    ('Agricultural','Agricultural'),
    ('Residential','Residential'),
    ('Commercial','Commercial'),
    ('Industry','Industry'),
    ('Public','Public'),
    ('Public','Public'),
    ('Reserve','Reserve'),
)

transaction_status_types = (
    ('Lodge','Lodge'),
    ('Validate','Validate'),
    ('Start','Start'),
    ('Assign','Assign'),
    ('Un-Assign','Un-Assign'),
    ('Dispatch','Dispatch'),
)

status_type= (
    ('Current','Current'),
    ('Historic','Historic'),
    ('Pending','Pending'),
    ('Previous','Previous'),
)

change_actions = (
    ('Update','Update'),
    ('Delete','Delete'),
    ('Insert','Insert'),
)

service_status_types = (
    ('Lodged','Lodged'),
    ('Validated','Validated'),
    ('Started','Started'),
    ('Assigned','Assigned'),
    ('Un-Assigned','Un-Assigned'),
    ('Dispatched','Dispatched'),
    ('Complteted','Completed'),
    ('Archived','Archived'),
)

ladm_badminunit_type = (
    ('Freehold title','Freehold title'),
    ('Leasehold','Leasehold'),
    ('Mining contract','Mining contract'),
    ('Conservation','Conservation'),
)

application_status_types = (
    ('Lodged','Lodged'),
    ('Validated','Validated'),
    ('Started','Started'),
    ('Assigned','Assigned'),
    ('Un-assigned','Un-assigned'),
    ('Dispatched','Dispatched'),
    ('Completed','Completed'),
    ('Archived','Archived'),
)

application_types = (
    ('Registration','Registration'),
    ('Official Search','Official Search'),
    ('Change of User','Change of User'),
)

landuse_restrictions_types = (
    ('Permitted Use','Permitted Use'),
    ('Non-permitted Use','Non-permitted Use'),
    ('Consented Use','Consented Use'),
    ('Actual Use','Actual Use'),
)

id_types = (
    ('National ID','National ID'),
    ('Passport','Passport'),
    ('Company Registration Number','Company Registation Number'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(Settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    telnumber = models.CharField(max_length=13,verbose_name='Telephone Number')
    address = models.CharField(max_length=50,verbose_name='Address',blank=True)
    def __str__(self):
        return '{}'.format(self.user.username)
    class Meta:
        verbose_name_plural = 'User Profiles'

class Customer(User):       ## Who is customer ? What makes them different from UserProfile model,
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Customer Account'
        verbose_name_plural = 'Customer Accounts'

class Staff(User):    
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Staff Account'
        verbose_name_plural = 'Staff Accounts'

class ladm_badminunit(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    type_code = models.CharField(max_length=50,choices=ladm_badminunit_type)
    parcel_id = models.ForeignKey('las_parcel')
    party_id = models.ForeignKey('las_party')
    admindocumenturi = models.ForeignKey('Documents')
    creation_date = Models.DateField()
    
    def __str__(self):
        return "{}".format(self.type_code)
    class Meta:
        verbose_name_plural = 'LADM_BAUnit'

class AdministrationArea(models.Model):
    unitid = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)
    class Meta:
        verbose_name_plural = 'Administrative Area'    
        managed = True ## The database manages this model

class RegistrationSection(gis_models.Model):
    sectionid = models.IntegerField(primary_key=True,unique=True)
    adminarea = models.ForeignKey(AdministrationArea)
    name = models.CharField(max_length=50)
    length = models.FloatField()
    area = models.FloatField()
    geom = gis_models.PolygonField(srid=21037)
    objects = gis_models.GeoManager()

    def __str__(self):
        return "{}".fomat(self.name)
    class Meta:
        verbose_name_plural = 'Registration Sections'   

class RegistrationBlock(gis_models.Model):
    blockid = models.IntegerField(primary_key=True,unique=True)
    sectionid = models.ForeignKey(RegistrationSection)
    name = models.CharField(max_length=50)
    leng = models.FloatField()
    geom = gis_models.PolygonField(srid=21037)
    objects = gis_models.GeoManager()

    def __str__(self):
        return "{}".format(self.name)
    class Meta:
        verbose_name_plural = 'Registration Blocks'

class las_parcel(gis_models.Model):       ## what is the unique parcel identifier -----> how have we arrived to it
    id = gis_models.IntegerField(primary_key=True,unique=True)
    blockid = models.IntegerField(null=True,blank=True)
    areacode = models.IntegerField(null=True,blank=True)
    blockname = models.CharField(max_length=50,null=True,blank=True)
    parcel_no = models.CharField(max_length=50,null=True,blank=True)
    sectcode = models.IntegerField(null=True,blank=True)
    land_use = models.ForeignKey('landuse_zoning',null=True,blank=True)
    surveyornumber = models.CharField(max_length=50,null=True,blank=True)
    surveydocid = models.CharField(max_length=50,null=True,blank=True)
    approval_date = models.DateTimeField(null=True,blank=True)
    historic_datetime  = models.DateTimeField(null=True,blank=True)
    parent = models.CharField(max_length=15,default='null',blank=True)
    area = models.FloatField()
    length = models.FloatField()
    objects = gis_models.GeoManager()

    def __str__(self):
        return  "{}".format(self.parcel_no)
    class Meta:
        verbose_name_plural = 'LADM_Parcel'

class Restrictions(models.Model):           ## what relationship exists between Restrictions and the Party
    restriction_id = models.IntegerField(primary_key=True,unique=True)
    adminunit = models.ForeignKey(ladm_badminunit)
    restriction_type = models.CharField(max_length=50,choices=restriction_types)
    restriction_Description = models.CharField(max_length=50)
    restriction_holder = models.CharField(max_length=50)
    amount = models.IntegerField()      ## Amount of  what ???
    
    def __str__(self):
        return  "{}".format(self.restriction_type)
    class Meta:
        verbose_name_plural = 'Restrictions'    

class LandUse_Restriction(models.Model):
    id = models.IntegerField(primary_key=True)
    adminunit = models.ForeignKey(ladm_badminunit)
    landuserestriction_type = models.CharField(max_length=50,choices=landuse_restrictions_types)        
    landrestriction_desc = models.TextField(max_length=100)
    registration_date = models.DateTimeField()
    objects = models.Manager()

    def __str__(self):
        return "{}".format(self.landuserestriction_type)
    class Meta:
        verbose_name_plural = 'Land Use Restrictions'    

class unverifiedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Unverified')

class verifiedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Verified')

class approvedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Approved')

class rejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Rejected')

class completedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Completed') 



###-----PLEASE CHECK THESE FUNCTIONS, uploading a file
def upload_application(instance,filename):
    return '/'.join(['application_docs',str(instance.id_number),filename])


def upload_report(instance,filename):
    return "report_images/%s" % (filename)


def upload_docs(instance,filename):
    return "documents/%s" % (filename)


class las_application(models.Model):
    app_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_type = models.CharField(max_length=20,null=True,choices=id_types,default=id_types[0][0])  
    id_number = models.CharField(max_length=15,null=True)
    parcel_number = models.CharField(max_legth=15,null=True)
    email = models.EmailField(max_length=50,default='franklinkzbenz95@gmail.com')
    telephone = models.CharField(max_length=50,help_text = 'Enter phone number')
    applicant_type = models.CharField(choices=agent_types,max_length=50)
    date_applied = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateField(null=True,blank=True)
    date_approved = models.DateField(null=True,blank=True)
    application_type = models.CharField(max_length=50,choices=application_types)
    title = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of Title')
    search = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of Search Document')
    comment = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of comment form')
    add_comment = models.FileField(upload_to=upload_application,null=True,help_text='Upload other comments if available*')
    scheme = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of Physical Scheme Plan')
    ppa = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of PPA2')
    receipt = models.FileField(upload_to=upload_application,null=True,help_text = 'Upload copy of payment receipt')  
    planning = models.FileField(upload_to=upload_application,null=True,help_text='Upload copy of planning document')
    status = models.CharField(max_length=15,null=True,choices=application_status,default=application_status[0][0])
    registry_comments = models.TextField(max_length=256,null=True,help_text='Registry section comments here')      
    dc_comments = models.TextField(max_length=256,null=True,help_text='Development control comments here')      
    upload_dcreport = models.FileField(upload_to=upload_report,null=True)
    final_comments = models.TextField(max_length=256,help_text='Final Comment here',null=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return '{}'.format(self.id_number)

    class Meta:
        verbose_name_plural = 'LADM_Application'
    class Meta:
        permissions = (
            ('view application','can verify application'),
        )


###########----------<><><><><><><> Get the meaning, extends las_application
class development(las_application):
    approved = verifiedManager()
    class Meta :
        proxy = True
        verbose_name_plural = 'Development_apps'

class registry(las_application):
    approved  = unverifiedManager()
    class Meta:
        proxy = True
        verbose_name_plural = 'Approved Apps'

class rejected(las_application):
    approved  = rejectedManager()
    class Meta:
        proxy =True   ### what is this ??
        verbose_name_plural = 'Rejected Apps'

class completed(las_application):
    approved = completedManager()
    class Meta:
        proxy = True
        verbose_name_plural = 'Completed Apps'

class dev_controlunit(models.Model):
    las_application = models.OneToOneField(las_application)
    user = models.ForeignKey(User)
    dc_verified = models.NullBooleanField(blank=True,null=True,default=None)
    dc_comments = models.TextField(max_length=256,null=True,blank=True,help_text='Development control comments here')
    date_checked = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Development Sections'

class la_party(models.Model): 
    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','N/A'),
    )       
    preffered_comm_methods = (
        ('Email','Email'),
        ('Mobile','Mobile'),
        ('Tel','Telephone'),
    )
    id = models.IntegerField(primary_key=True)
    ext_id = models.CharField(max_length=50)
    partytype = models.CharField(max_length=50,choices=party_types)
    name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    gender_code = models.CharField(max_length=50,choices=GENDER_CHOICES)
    id_type_code = models.CharField(choices=id_types,blank=True)
    id_number = models.CharField(max_length=50)


    ## look at Django Hstore
    address_id = models.CharField(max_length=50)
    email = models.EmailField(blank=True,null=True)
    mobile = models.CharField(max_length=13,null=True,blank=True)
    preffred_communication = models.CharField(max_length=50,choices=preffered_comm_methods,blank=True,null=True)
    
    def __str__(self):
        return '{} {}'.format(self.name,self.id_number)
    class Meta:
        verbose_name_plural = 'LA_Party'

class transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    from_application_id = models.ForeignKey('las_application')
    assigned = models.BooleanField()
    assignee_id = models.ForeignKey('UserProfile') 
    assigned_date = models.DateTimeField()
    status = models.CharField(choices=transaction_status_types,max-max_length=50)
    approval_datetime = models.DateTimeField()
    service_fee = models.IntegerField()
    fee_paid = models.BooleanField()
    change_action = models.CharField(max_length=50,choices=change_actions)         
    change_user = models.CharField(max_length=50)
    notes = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.id,self.assignee_id)  
    class Meta:
        verbose_name_plural = 'Transcations'

class valuation(models.Mode):
    valuation_id = models.IntegerField(primary_key=True)
    badminunit = models.ForeignKey(ladm_badminunit)
    value_amount = models.IntegerField()
    valuationstartdate = models.DateTimeField()
    valuationenddate = models.DateTimeField()

    def __str__(self):
        return '{} {}'.format(self.valuation_id,self.badminunit)

    class Meta:
        verbose_name_plural = 'Valuation'

class Documents(models.Model):
    id = models.IntegerField()
    of_type = models.CharField(max_length=20)
    document_name = models.CharField(max_length=50,blank=False,null=False)
    document_image = models.FileField(upload_to=upload_docs,null=True)
    datetime_uploaded = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.document_name)
    class Meta:
        verbose_name_plural = 'Uploaded Documents'    



    






























