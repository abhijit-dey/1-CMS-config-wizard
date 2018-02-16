
import requests
import ccw_lib
import urllib3
from appJar import gui

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)     # hiding the InsecureRequestWarning at the start
urllib3.disable_warnings(urllib3.exceptions.HTTPError)

# Global variable defined here. 
cms_ip                      = ""
cms_webadmin_port           = ""
cms_objects                 = "coSpaces"
cms_object                  = cms_objects[:-1]
cms_url_system_status       = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/system/status"
cms_url                     = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
cms_webadmin_authorization  = ""
cms_webadmin_content_type   = ""
cms_login                   = ""
cms_password                = ""


def login_window_button_press(name):
    if name == "Submit":
        global cms_ip
        global cms_webadmin_port
        global cms_login
        global cms_password
        global cms_webadmin_authorization
        global cms_webadmin_content_type
        global cms_url_system_status

        cms_ip = app.getEntry("cms_ip")
        #print(cms_ip)
        cms_webadmin_port = app.getEntry("cms_webadmin_port")
        #print(cms_webadmin_port)
        cms_login = app.getEntry("cms_login")
        cms_password = app.getEntry("cms_password")
        #cms_webadmin_authorization = app.getEntry("cms_webadmin_authorization")
        #cms_webadmin_content_type = app.getEntry("cms_webadmin_content_type")
        creds_checkbox = app.getCheckBox("Remember Credentials")

        success_msg = "Login into "+cms_ip+" Successful."
        error_msg = "Not able to login into your CMS"

        cms_url_system_status       = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/system/status"
        r = ccw_lib.cms_login_status(cms_url_system_status, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, \
            cms_password)

        check = 0
        if r == 200:
            #print(r.text)
            check = 1

        if check == 1:
            if creds_checkbox == True:
                f = open("login_info", "w")
                f.write(cms_ip)
                f.write(";")
                f.write(cms_webadmin_port)
                f.write(";")
                f.write(cms_login)
                f.write(";")
                f.write(cms_password)
                f.write(";")
                f.close()

            app.infoBox("Success", success_msg)
            app.hideSubWindow("login_window")
            app.go()
        elif check == 0:
            app.errorBox("Error", error_msg)
    elif name == "Clear":
        app.clearAllEntries()
        app.setFocus("cms_ip")
        #app.setEntryDefault("cms_webadmin_authorization", "e.g. Basic YWRtaW46dG1lYmxyMTIz")
        #app.setEntryDefault("cms_webadmin_content_type", "e.g. application/x-www-form-urlencoded; charset=utf-8")
    elif name == "Exit":
    	app.stop()
    elif name == "Print":
        print(cms_ip)
        print(cms_webadmin_port)

def press(name):
    if name == "Quit":
        app.stop()
    elif name == "Login Info":
        app.showLabelFrame("Login Info:")
        app.hideLabelFrame("View Spaces:")
    
    elif name == "View Spaces":
        cms_objects = "coSpaces"
        cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
        r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)

        cms_object = cms_objects[:-1]
        text = ccw_lib.get_object_formated (r.text, cms_object)
        number_of_coSpaces = ccw_lib.get_number_of_objects (r, cms_objects)

        coSpaces_id_list = ccw_lib.get_object_id_list (cms_objects, cms_ip, number_of_coSpaces, cms_webadmin_port, \
            cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
        coSpaces_name_list = []
        coSpaces_uri_list = []
        for i in range(0,number_of_coSpaces):
            cms_objects = "coSpaces/"+coSpaces_id_list[i]
            cms_object = cms_objects[:-1]
            cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
            r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
            parameter = "name"
            value = ccw_lib.get_parameter_from_1_get(r.text, parameter)
            coSpaces_name_list.append(value)
            parameter = "uri"
            value = ccw_lib.get_parameter_from_1_get(r.text, parameter)
            coSpaces_uri_list.append(value)

        app.openLabelFrame("View Spaces:")
        app.setLabel("l21", number_of_coSpaces)
        for a in range(0,number_of_coSpaces):
            rowLabel = "row"+str(a+1)+"col1"
            app.setLabel(rowLabel, coSpaces_name_list[a])
        for a in range(0,number_of_coSpaces):
            rowLabel = "row"+str(a+1)+"col2"
            app.setLabel(rowLabel, coSpaces_uri_list[a])
        app.stopLabelFrame()
        app.showLabelFrame("View Spaces:")
        app.hideLabelFrame("Login Info:")

def back_to_menu(name):
    pass

def viewSpaceRow1Details(name):
    pass

def viewSpaceRow1Edit(name):
    pass


app = gui("CMS Configuration Wizard")

app.setStretch("none")
app.setFont(15)
app.setGeometry(800, 400)

app.addStatusbar(header="", fields=2, side="RIGHT")
app.setStatusbarWidth(12, field=0)
app.setStatusbar("Version 1.5", field=0)
app.setStatusbarWidth(30, field=1)
app.setStatusbar("Feedback - abdey@cisco.com", field=1)

app.addLabel("ph1", "", 0,0)
app.setLabelWidth("ph1", 20)
app.addLabel("ph2", "", 0,1)
#app.setLabelWidth("ph2", 1000)

app.startLabelFrame("Menu:", 0,0)
app.setLabelFrameAnchor("Menu:", "n")
app.setSticky("n")
app.addLink("Login Info", press, 1,0)
app.addLink("View Spaces", press, 2,0)
app.addLink("Quit", press, 3,0)
app.stopLabelFrame()
app.showLabelFrame("Menu:")

app.startLabelFrame("Login Info:", 0,1)
try:
    f = open("login_info", "r")
    info = f.read()
    creds = info.split(";")
    f.close()
except FileNotFoundError:
    pass
app.setStretch("none")
app.setFont(15)
app.addLabel("l7", "Web-Admin IP:", 0,1)
app.addEntry("cms_ip2", 0,2)
if creds[0]:
    app.setEntry("cms_ip2", creds[0], callFunction=False)
app.setFocus("cms_ip2")
app.addLabel("l8", "Web-Admin Port:", 1,1)
app.addEntry("cms_webadmin_port2", 1,2)
if creds[1]:
    app.setEntry("cms_webadmin_port2", creds[1])
app.addLabel("l9", "Username:", 2,1)
app.addEntry("cms_login2", 2,2)
if creds[2]:
    app.setEntry("cms_login2", creds[2])
app.addLabel("l10", "Password:", 3,1)
app.addSecretEntry("cms_password2", 3,2)
if creds[3]:
    app.setEntry("cms_password2", creds[3])
app.addCheckBox(" Remember Credentials", 6,2)
app.addButtons([" Submit", " Clear"], login_window_button_press, 7,2)
app.stopLabelFrame()
app.hideLabelFrame("Login Info:")

app.startLabelFrame("View Spaces:", 0,1)
app.addLabel("l20", "Total Number of Spaces = ", 1,0)
app.addLabel("l21", "", 1,1)
app.addLabel("l15", " Name ", 3,0)
app.setLabelRelief("l15", "groove")
app.addLabel("l11", " Primary URI ", 3,1)
app.setLabelRelief("l11", "groove")
app.addLabel("l13", " Options ", 3,2)
app.setLabelRelief("l13", "groove")
# app.addLink("Details", viewSpaceRow1Details, 4,2)
# app.addLink("Edit", viewSpaceRow1Edit, 4,3)
numberOfColumns = 30
for a in range(1,numberOfColumns):
    rowLabel = "row"+str(a)+"col1"
    rowNumber = a+4
    app.addLabel(rowLabel, "", rowNumber,0)
for a in range(1,numberOfColumns):
    rowLabel = "row"+str(a)+"col2"
    rowNumber = a+4
    app.addLabel(rowLabel, "", rowNumber,1)
app.stopLabelFrame()
app.hideLabelFrame("View Spaces:")





# This is the initial login window (sub window).
app.startSubWindow("login_window")
try:
    f = open("login_info", "r")
    info = f.read()
    creds = info.split(";")
    f.close()
except FileNotFoundError:
    pass
app.setStretch("none")
app.setFont(15)
app.addLabel("l3", "Web-Admin IP:", 0,1)
app.addEntry("cms_ip", 0,2)
if creds[0]:
    app.setEntry("cms_ip", creds[0], callFunction=False)
app.setFocus("cms_ip")
app.addLabel("l4", "Web-Admin Port:", 1,1)
app.addEntry("cms_webadmin_port", 1,2)
if creds[1]:
    app.setEntry("cms_webadmin_port", creds[1])
app.addLabel("l5", "Username:", 2,1)
app.addEntry("cms_login", 2,2)
if creds[2]:
    app.setEntry("cms_login", creds[2])
app.addLabel("l6", "Password:", 3,1)
app.addSecretEntry("cms_password", 3,2)
if creds[3]:
    app.setEntry("cms_password", creds[3])
#app.addLabel("l7", "Authentication:", 4,1)
#app.addEntry("cms_webadmin_authorization", 4,2)
#app.setEntryWidth("cms_webadmin_authorization", 35)
#app.setEntryDefault("cms_webadmin_authorization", "e.g. Basic YWRtaW46dG1lYmxyMTIz")
#app.setEntryAlign("cms_webadmin_authorization", "left")
#app.addLabel("l8", "Content Type:", 5,1)
#app.addEntry("cms_webadmin_content_type", 5,2)
#app.setEntryWidth("cms_webadmin_content_type", 50)
#app.setEntryDefault("cms_webadmin_content_type", "e.g. application/x-www-form-urlencoded; charset=utf-8")
#app.setEntryAlign("cms_webadmin_content_type", "left")
app.addCheckBox("Remember Credentials", 6,2)
app.addButtons(["Submit", "Clear", "Exit"], login_window_button_press, 7,2)
app.stopSubWindow()


app.go(startWindow="login_window")





















