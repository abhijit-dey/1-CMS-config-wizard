
import requests
import ccw_lib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)		# hiding the InsecureRequestWarning at the start
urllib3.disable_warnings(urllib3.exceptions.HTTPError)


print("\nCMS Configuration Wizard, version 1.4\n")


# Global Variable Initialization
cms_creds = ccw_lib.read_creds_from_file("CMS Credentials")

cms_ip 						= cms_creds[0]
cms_webadmin_port 			= cms_creds[1]
cms_objects 				= "coSpaces"
cms_object 					= cms_objects[:-1]
cms_url_system_status		= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/system/status"
cms_url  					= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
cms_webadmin_authorization 	= cms_creds[2]
cms_webadmin_content_type 	= cms_creds[3]
cms_login 					= cms_creds[4]
cms_password 				= cms_creds[5]

code_exit_message 			= "\n\nThanks for using my code - Abhijit Dey,\n\
Please give feedback at (abdey@cisco.com)\n"


# Check CMS connection, before proceeding into the code.
print("\n  Info - Logging into CMS.")
r = ccw_lib.cms_login_status(cms_url_system_status, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, \
	cms_password)
if r==200:
	print("  Info - Logging Successful.")
else:
	print("  Info - Logging Failed.")
	quit()

menu_1	= "\nWhat do you want to Configure?\n\
  1. Space\n\
  2. Making Participant Important in Active Conference\n\
  3. LDAP Integration for User Import. (Under Construction)\n\
  4. Assigning Users with PMP+ for already imported users. (Under Construction)\n\
  5. Configuring Recording. (Under Construction)\n\
  6. Configuring Streaming. (Under Construction)\n\
  c. Cancel\n\
  q. Exit\n\
  "
menu_11	= "Space\n\
  1. Create New Space\n\
  2. Modify Existing Space\n\
  c. Cancel\n\
  q. Exit\n\
  "

# Options Menu 
while 1:
	menu_1_response = input(menu_1)
	if menu_1_response=="1":
		menu_11_response = input(menu_11)
		if menu_11_response=="1":
			coSpace_parameters_list = []
			coSpace_parameters_list = ccw_lib.list_for_space_creation(coSpace_parameters_list)

			space_coSpace_parameters_list = ccw_lib.get_coSpace_parameters_from_list()
			space_coSpace_callProfile_parameters_list = ccw_lib.get_coSpace_callProfile_parameters_from_list()
			space_coSpace_callLegProfile_parameters_list = ccw_lib.get_coSpace_callLegProfile_parameters_from_list()
			space_coSpace_callBrandingProfile_parameters_list = ccw_lib.get_coSpace_callBrandingProfile_parameters_from_list()

			cms_objects = "callLegProfiles"
			cms_object 	= cms_objects[:-1]
			cms_url  	= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			callLegProfile_id = ccw_lib.create_new_object(cms_objects, cms_ip, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			ccw_lib.put_fields (space_coSpace_callLegProfile_parameters_list, cms_object, cms_url, \
				callLegProfile_id, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)			

			cms_objects = "callProfiles"
			cms_object 	= cms_objects[:-1]
			cms_url  	= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			callProfile_id = ccw_lib.create_new_object(cms_objects, cms_ip, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			ccw_lib.put_fields (space_coSpace_callProfile_parameters_list, cms_object, cms_url, \
				callProfile_id, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)

			cms_objects = "callBrandingProfiles"
			cms_object 	= cms_objects[:-1]
			cms_url  	= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			callBrandingProfile_id = ccw_lib.create_new_object(cms_objects, cms_ip, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			ccw_lib.put_fields (space_coSpace_callBrandingProfile_parameters_list, cms_object, cms_url, \
				callBrandingProfile_id, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)

			space_coSpace_parameters_list ["callBrandingProfile"] = callBrandingProfile_id
			space_coSpace_parameters_list ["callLegProfile"] = callLegProfile_id
			space_coSpace_parameters_list ["callProfile"] = callProfile_id

			cms_objects = "coSpaces"
			cms_object 	= cms_objects[:-1]
			cms_url  	= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			coSpace_id = ccw_lib.create_new_object(cms_objects, cms_ip, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			ccw_lib.put_fields (space_coSpace_parameters_list, cms_object, cms_url, \
				coSpace_id, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			#break
		elif menu_11_response=="2":

			r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)

			cms_object = cms_objects[:-1]
			text = ccw_lib.get_object_formated (r.text, cms_object)

			number_of_coSpaces = ccw_lib.get_number_of_objects (r, cms_objects)

			coSpaces_id_list = ccw_lib.get_object_id_list (cms_objects, cms_ip, number_of_coSpaces, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			coSpaces_name_list = []
			for i in range(0,number_of_coSpaces):
				cms_objects = "coSpaces/"+coSpaces_id_list[i]
				cms_object = cms_objects[:-1]
				cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
				r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
				parameter = "name"
				value = ccw_lib.get_parameter_from_1_get(r.text, parameter)
				coSpaces_name_list.append(value)
			#print(number_of_coSpaces)

			print("\nList of coSpaces:")
			for i in range(0,number_of_coSpaces):
				list_num = i+1
				print(str(list_num)+". Space Name = "+coSpaces_name_list[i]+" with coSpace id = "+coSpaces_id_list[i])

			coSpace_id = input("Enter the coSpace id : ")

			coSpace_parameters_list = []
			coSpace_parameters_list = ccw_lib.list_for_space_modification(coSpace_parameters_list)
			space_coSpace_parameters_list = ccw_lib.get_coSpace_parameters_from_list()
			print(space_coSpace_parameters_list)

			cms_objects = "coSpaces"
			cms_object = cms_objects[:-1]
			cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			ccw_lib.put_fields (space_coSpace_parameters_list, cms_object, cms_url, \
				coSpace_id, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
		elif menu_11_response=="q":
			print(code_exit_message)
			break
		else :
			print("Wrong Input!"+code_exit_message)
	elif menu_1_response=="2":		
		calls_id_list = []
		calls_list_space_name = []
		calls_list_space_id = []
		#print("    Log - calls_id_list ")
		#print(calls_id_list)
		#print("    Log - calls_list_space_name ")
		#print(calls_list_space_name)
		#print("    Log - calls_list_space_name ")
		#print(calls_list_space_name)

		cms_objects 				= "calls"
		cms_object 					= cms_objects[:-1]
		cms_url  					= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
		#print("    Log - cms_url "+cms_url)

		calls_get_handle = ccw_lib.api_get(cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, \
			cms_password)
		number_of_calls = ccw_lib.get_number_of_objects(calls_get_handle, cms_objects)
		#print("    Log - number_of_calls "+str(number_of_calls))

		if number_of_calls == 0:
			print("No Active Conferences.")
			input("Hit Enter to quit!")
			print(code_exit_message)
			break
		calls_id_list = ccw_lib.get_object_id_list(cms_objects, cms_ip, number_of_calls, cms_webadmin_port, \
			cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
		#print("    Log - calls_id_list ")
		print(calls_id_list)

		for i in range(0,len(calls_id_list)):
			calls_list_space_id.append(calls_id_list[i])
			
			cms_objects  				= "calls/"+calls_id_list[i]
			cms_object 					= cms_objects[:-1]
			cms_url  					= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			parameter = "name"
			value = ccw_lib.get_parameter_from_1_get(r.text, parameter)
			#print("    Log - value "+value)
			calls_list_space_name.append(value)
		
		#print("    Log - calls_list_space_name ")
		print(calls_list_space_name)

		print("\n\nImportant Participant for which Conference?")
		for i in range(0,len(calls_list_space_name)):
			print(i+1,"Conference Name -",calls_list_space_name[i],"with id =",calls_list_space_id[i])
		choice_calls = input("Enter the number before Conference Name (e.g. 1 for 1st participant): ")
		choice_calls = int(choice_calls)
		choice_calls = choice_calls-1

		cms_objects = "calls/"+calls_list_space_id[choice_calls]+"/participants/"
		cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
		#print("    Log - cms_url "+cms_url)
		r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
		number_of_calls = ccw_lib.get_number_of_objects_new (r.text, "participants")
		#print("    Log - number_of_calls "+str(number_of_calls))

		calls_participants_id_list = []
		calls_participants_name_list = []

		calls_participants_id_list = ccw_lib.get_object_id_list("participants", cms_ip, number_of_calls, cms_webadmin_port, \
			cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
		#print("    Log - calls_participants_id_list ")
		#print(calls_participants_id_list)

		for i in range(0,len(calls_participants_id_list)):
			cms_objects = "calls/"+calls_list_space_id[choice_calls]+"/participants/"+calls_participants_id_list[i]
			cms_url  					= "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
			#print("    Log - cms_url "+cms_url)
			r = ccw_lib.api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			calls_participants_name_list.append(ccw_lib.get_parameter_from_1_callLeg(r.text, "<name>"))
		#print("    Log - calls_participants_name_list ")
		#print(calls_participants_name_list)

		call_selection = 0
		while call_selection != "q":
			print("\n\nList of participants :")
			for i in range(0,len(calls_participants_name_list)):
				print(i+1,"Participant ",calls_participants_name_list[i],"with participant id",calls_participants_id_list[i])	
			call_selection = input("Select the number (e.g. 1 for 1st participant) before Participant (Enter q to quit): ")
			#print("    Log - call_selection "+call_selection)
			if call_selection != "q":
				call_priority = input("Enter the important priority for the selected participant (0 - 100): ")
				call_selection = int(call_selection)
				cms_objects = "calls/"+calls_list_space_id[choice_calls]+"/participants/"+\
					calls_participants_id_list[call_selection-1]
				#print("    Log - calls_participants_id_list "+calls_participants_id_list[call_selection-1])

				cms_object = "participant"
				cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
				print("    Log - cms_url "+cms_url)
				object_parameters = {"importance": call_priority}
				r = requests.put(
				            url=cms_url,
				            headers={
				                "Authorization": cms_webadmin_authorization,
				                "Content-Type": cms_webadmin_content_type,
				            },
				            auth=(cms_login, cms_password),
				            verify=False,
				            data=object_parameters 		# object_parameters should be a dictionary in following format
				            							# object_parameters = {recordingMode: manual}
				       )
				if r.status_code == 200:
					print("Updated the ",object_parameters,".")
				else:
					print("Error updating the",object_parameters,".")
		#break
	elif menu_1_response=="q":
		print(code_exit_message)
		break
	else :
		print("Wrong Input!"+code_exit_message)
		#break

