
import requests


space_coSpace_parameters_list = {}
space_coSpace_callProfile_parameters_list = {}
space_coSpace_callLegProfile_parameters_list = {}
space_coSpace_callBrandingProfile_parameters_list = {}


# Input filename with the CMS creds.
# Returns the list of CMS creds. 
def read_creds_from_file(file_name):
	print("  Info - Getting CMS credentials from the file.")
	f = open(file_name, "r")
	lines_list = f.readlines()
	f.close()

	temp_list = []
	temp_list = lines_list[0].split(" ")
	cms_ip = temp_list[3]

	temp_list = []
	temp_list = lines_list[1].split(" ")
	cms_webadmin_port = temp_list[4]

	temp_list = []
	temp_list = lines_list[2].split(" ")
	cms_webadmin_authorization = temp_list[4]+" "+temp_list[5]

	temp_list = []
	temp_list = lines_list[3].split(" ")
	cms_webadmin_content_type = temp_list[5]+" "+temp_list[6]

	temp_list = []
	temp_list = lines_list[4].split(" ")
	cms_login = temp_list[3]

	temp_list = []
	temp_list = lines_list[5].split(" ")
	cms_password = temp_list[3]

	cms_creds = [cms_ip, cms_webadmin_port, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password]
	for i in range(0,len(cms_creds)):
		if cms_creds[i] == None:
			print("  Error - CMS Credentials not found.")
		else:
			print("  Info - CMS Credentials Found")

	return cms_creds


def cms_login_status(cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password):
	r = requests.get(
            url=cms_url,
            headers={
                #"Authorization": cms_webadmin_authorization,
                "Content-Type": cms_webadmin_content_type,
            },
            auth=(cms_login, cms_password),
            verify=False,
            timeout=2.00
        )
	#print(r.text)
	return r.status_code


# Issues GET API and returns the handle. 
def api_get(cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password):
	print("  Info - Issuing GET API command.")
	r = requests.get(
	            url=cms_url,
	            headers={
	                "Authorization": cms_webadmin_authorization,
	                "Content-Type": cms_webadmin_content_type,
	            },
	            auth=(cms_login, cms_password),
	            verify=False
		)
	print("  Info - GET API success.")
	return r

# Inputs a standard GET response and formats it into readable format. 
def get_object_formated(get_raw_content, cms_object):
	print("  Info - Formatting output of standard GET response.")

	get_raw_content = get_raw_content.replace ("><", ">\n<")
	get_raw_content = get_raw_content.replace ("<"+cms_object+" total", "\n\n"+cms_object+" total")
	get_raw_content = get_raw_content.replace ("\n<", "\n")
	get_raw_content = get_raw_content.replace (">\n", "\n")
	before = cms_object+" id"
	after = "\n"+cms_object+" id"
	get_raw_content = get_raw_content.replace (before, after)

	print("  Info - GET Response Formatted.")
	return get_raw_content

# Issues POST API command and returns the handle
def api_post(cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password):
	r = requests.post(
	            url=cms_url,
	            headers={
	                "Authorization": cms_webadmin_authorization,
	                "Content-Type": cms_webadmin_content_type,
	            },
	            auth=(cms_login, cms_password),
	            verify=False
	)
	return r

# Issues PUT API command and returns the handle.
# cms_url is without the object_id
# object_parameters should be a dictionary, syntax = {recordingMode: manual}
def api_put(cms_url, object_id, object_parameters, cms_webadmin_authorization, cms_webadmin_content_type, \
	cms_login, cms_password):
	print("  Info - Updating the "+object_id+".")
	#print("Log - ", object_id)
	cms_url = cms_url+"/"+object_id
	#print("Log - ", cms_url)
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
		print("  Info - Updated the ",object_parameters,".")
	else:
		print("  Info - Error updating the",object_parameters,".")
	return r


menu_defaultLayout = "Default Layout:\n\
  1. All Equal\n\
  2. Speaker Only\n\
  3. TelePresence\n\
  4. Stacked\n\
  5. All Equal Quarters\n\
  6. All Equal Ninths\n\
  7. All Equal Sixteenths\n\
  8. All Equal Twenty-Fifths\n\
  9. onePlusFive\n\
  10. onePlusSeven\n\
  11. onePlusNine\n\
  12. automatic\n\
  13. onePlusN\n\
  "

menu_true_false = "\
  1. True (default)\n\
  2. False\n\
  "

menu_true_false_default = "\
  1. True\n\
  2. False (default)\n\
  "
menu_presentation_display_mode = "\
  1. Dual Stream\n\
  2. Single Stream\n\
  "

menu_callLegProfiles_auto_disabled = "\
  1. Auto\n\
  2. Disabled (audio-only participant)\n\
  "

menu_sipMediaEncryption = "\
  1. Optional\n\
  2. Required\n\
  3. Prohibited\n\
  "

menu_callLegProfile_deactivationMode = "\
  1. Deactivate\n\
  2. Disconnect\n\
  3. Remain Activated\n\
  "

menu_callLegProfile_bfcpMode = "\
  1. Server Only (normal setting for SIP Endpoints)\n\
  2. Server And Client (with a remote conference-hosting device such as a third party MCU)\n\
  "

menu_callLegProfile_qualityMain = "\
  1. Unrestricted (max 1080p60)\n\
  2. Max 1080p30\n\
  3. Max 720p30\n\
  4. Max 480p30\n\
  "

menu_callLegProfile_qualityPresentation = "\
  1. Unrestricted (max 1080p60)\n\
  2. Max 1080p30\n\
  3. Max 720p5\n\
  "

menu_callLegProfile_participantCounter = "\
  1. Never\n\
  2. Auto (default)(shows only when more participants than can be seen On-Sreen)\n\
  3. Always\n\
  "

menu_callProfile_recordingMode = "\
  1. Disabled\n\
  2. Manual (default)\n\
  3. Automatic\n\
  "

menu_callProfile_passcodeMode = "\
  1. Required (requires passcode to be entered, with blank passcode needing to be explicitly entered)\n\
  2. Timeout (after an amount of time has elapsed with no passcode being entered, interpret this as a blank passcode)\n\
  "

# Creates a list of all the parameters that the user needs in a space.
# Inputs an empty list and returns the same list with values. 
def list_for_space_creation(coSpace_parameters_list):
	
	while 1:
		coSpace_name = input("Name (Mandatory): ")
		if coSpace_name != "":
			coSpace_parameters_list.append(coSpace_name)
			break

	while 1:
		coSpace_uri = input("URI (Mandatory): ")
		if coSpace_uri != "":
			coSpace_parameters_list.append(coSpace_uri)
			break

	coSpace_secondary_uri = input("Secondary URI: ")
	coSpace_parameters_list.append(coSpace_secondary_uri)

	callProfile_participantLimit = ""
	callProfile_participantLimit = input("Conference - Maximum number of participants (default = no restrictions)?\n")
	coSpace_parameters_list.append(callProfile_participantLimit)

	callLegProfile_maxCallDurationTime = ""
	callLegProfile_maxCallDurationTime = input("Participant - Number of seconds the participant \
will be connected to the Conference (default = no restrictions)?\n")
	coSpace_parameters_list.append(callLegProfile_maxCallDurationTime)

	print("Participant - Can see the number of overflow participants?")
	callLegProfile_participantCounter = input(menu_callLegProfile_participantCounter)
	if callLegProfile_participantCounter == "1":
		callLegProfile_participantCounter = "never"
	elif callLegProfile_participantCounter == "2":
		callLegProfile_participantCounter = "auto"
	elif callLegProfile_participantCounter == "3":
		callLegProfile_participantCounter = "always"
	else :
		callLegProfile_participantCounter = ""
	coSpace_parameters_list.append(callLegProfile_participantCounter)

	coSpace_defaultLayout = input(menu_defaultLayout)
	if coSpace_defaultLayout == "1":
		coSpace_defaultLayout = "allEqual"
	elif coSpace_defaultLayout == "2":
		coSpace_defaultLayout = "speakerOnly"
	elif coSpace_defaultLayout == "3":
		coSpace_defaultLayout = "telepresence"
	elif coSpace_defaultLayout == "4":
		coSpace_defaultLayout = "stacked"
	elif coSpace_defaultLayout == "5":
		coSpace_defaultLayout = "allEqualQuarters"
	elif coSpace_defaultLayout == "6":
		coSpace_defaultLayout = "allEqualNinths"
	elif coSpace_defaultLayout == "7":
		coSpace_defaultLayout = "allEqualSixteenths"
	elif coSpace_defaultLayout == "8":
		coSpace_defaultLayout = "allEqualTwentyFifths"
	elif coSpace_defaultLayout == "9":
		coSpace_defaultLayout = "onePlusFive"
	elif coSpace_defaultLayout == "10":
		coSpace_defaultLayout = "onePlusSeven"
	elif coSpace_defaultLayout == "11":
		coSpace_defaultLayout = "onePlusNine"
	elif coSpace_defaultLayout == "12":
		coSpace_defaultLayout = "automatic"
	elif coSpace_defaultLayout == "13":
		coSpace_defaultLayout = "onePlusN"
	else :
		coSpace_defaultLayout = ""
	coSpace_parameters_list.append(coSpace_defaultLayout)

	print("Participant - can Change Layout?")
	callLegProfile_changeLayoutAllowed = input(menu_true_false)
	if callLegProfile_changeLayoutAllowed == "1":
		callLegProfile_changeLayoutAllowed = "true"
	elif callLegProfile_changeLayoutAllowed == "2":
		callLegProfile_changeLayoutAllowed = "false"
	else :
		callLegProfile_changeLayoutAllowed = ""
	coSpace_parameters_list.append(callLegProfile_changeLayoutAllowed)

	print("Participant - Pane Labels Visible?")
	callLegProfile_participantLabels = input(menu_true_false)
	if callLegProfile_participantLabels == "1":
		callLegProfile_participantLabels = "true"
	elif callLegProfile_participantLabels == "2":
		callLegProfile_participantLabels = "false"
	else :
		callLegProfile_participantLabels = ""
	coSpace_parameters_list.append(callLegProfile_participantLabels)

	print("Participant - Maximum main Video Call quality for this participant?")
	callLegProfile_qualityMain = input(menu_callLegProfile_qualityMain)
	if callLegProfile_qualityMain == "1":
		callLegProfile_qualityMain = "unrestricted"
	elif callLegProfile_qualityMain == "2":
		callLegProfile_qualityMain = "max1080p30"
	elif callLegProfile_qualityMain == "3":
		callLegProfile_qualityMain = "max720p30"
	elif callLegProfile_qualityMain == "2":
		callLegProfile_qualityMain = "max480p30"
	else :
		callLegProfile_qualityMain = ""
	coSpace_parameters_list.append(callLegProfile_qualityMain)

	print("Participant - Can Share Presentation?")
	callLegProfile_presentationContributionAllowed = input(menu_true_false)
	if callLegProfile_presentationContributionAllowed == "1":
		callLegProfile_presentationContributionAllowed = "true"
	elif callLegProfile_presentationContributionAllowed == "2":
		callLegProfile_presentationContributionAllowed = "false"
	else :
		callLegProfile_presentationContributionAllowed = ""
	coSpace_parameters_list.append(callLegProfile_presentationContributionAllowed)

	if callLegProfile_presentationContributionAllowed != "false":
		print("Participant - Maximum Presentation quality for this participant?")
		callLegProfile_qualityPresentation = input(menu_callLegProfile_qualityPresentation)
		if callLegProfile_qualityPresentation == "1":
			callLegProfile_qualityPresentation = "unrestricted"
		elif callLegProfile_qualityPresentation == "2":
			callLegProfile_qualityPresentation = "max1080p30"
		elif callLegProfile_qualityPresentation == "3":
			callLegProfile_qualityPresentation = "max720p5"
		else :
			callLegProfile_qualityPresentation = ""
		coSpace_parameters_list.append(callLegProfile_qualityPresentation)
	else :
		callLegProfile_qualityPresentation = ""
		coSpace_parameters_list.append(callLegProfile_qualityPresentation)

	if callLegProfile_presentationContributionAllowed != "false":
		print("Participant - Presentation Display Mode?")
		callLegProfile_presentationDisplayMode = input(menu_presentation_display_mode)
		if callLegProfile_presentationDisplayMode == "1":
			callLegProfile_presentationDisplayMode = "dualStream"
		elif callLegProfile_presentationDisplayMode == "2":
			callLegProfile_presentationDisplayMode = "singleStream"
		else :
			callLegProfile_presentationDisplayMode = ""
		coSpace_parameters_list.append(callLegProfile_presentationDisplayMode)

		print("Participant - Participant is permitted to perform presentation video channel operations (BFCP Mode)?")
		callLegProfile_sipPresentationChannelEnabled = input(menu_true_false)
		if callLegProfile_sipPresentationChannelEnabled == "1":
			callLegProfile_sipPresentationChannelEnabled = "true"
		elif callLegProfile_sipPresentationChannelEnabled == "2":
			callLegProfile_sipPresentationChannelEnabled = "false"
		else :
			callLegProfile_sipPresentationChannelEnabled = ""
		coSpace_parameters_list.append(callLegProfile_sipPresentationChannelEnabled)

		print("Participant - If last option is true, then BFCP Mode?")
		callLegProfile_bfcpMode = input(menu_callLegProfile_bfcpMode)
		if callLegProfile_bfcpMode == "1":
			callLegProfile_bfcpMode = "serverOnly"
		elif callLegProfile_bfcpMode == "2":
			callLegProfile_bfcpMode = "serverAndClient"
		else :
			callLegProfile_bfcpMode = ""
		coSpace_parameters_list.append(callLegProfile_bfcpMode)
	else :
		callLegProfile_presentationDisplayMode = ""
		coSpace_parameters_list.append(callLegProfile_presentationDisplayMode)
		callLegProfile_sipPresentationChannelEnabled = ""
		coSpace_parameters_list.append(callLegProfile_sipPresentationChannelEnabled)
		callLegProfile_bfcpMode = ""
		coSpace_parameters_list.append(callLegProfile_bfcpMode)

	print("Conference - Chat enabled in this Conference?")
	callProfile_messageBoardEnabled = input(menu_true_false)
	if callProfile_messageBoardEnabled == "1":
		callProfile_messageBoardEnabled = "true"
	elif callProfile_messageBoardEnabled == "2":
		callProfile_messageBoardEnabled = "false"
	else :
		callProfile_messageBoardEnabled = ""
	coSpace_parameters_list.append(callProfile_messageBoardEnabled)

	coSpace_passcode = input("Passcode to join this Space: ")
	coSpace_parameters_list.append(coSpace_passcode)

	print("Conference - Passcode Mode?")
	callProfile_passcodeMode = input(menu_callProfile_passcodeMode)
	if callProfile_passcodeMode == "1":
		callProfile_passcodeMode = "required"
	elif callProfile_passcodeMode == "2":
		callProfile_passcodeMode = "timeout"
	else :
		callProfile_passcodeMode = ""
	coSpace_parameters_list.append(callProfile_passcodeMode)

	callProfile_passcodeTimeout = ""
	callProfile_passcodeTimeout = input("Conference - the amount of time, in seconds, that the \
Conference will wait before before interpreting passcode as a blank passcode?\n")
	coSpace_parameters_list.append(callProfile_passcodeTimeout)

	coSpace_secret = input("Secret Key (Values entered in wrong format wont get updated): ")
	coSpace_parameters_list.append(coSpace_secret)

	print("Regenerate Secret?")
	coSpace_regenerateSecret = input(menu_true_false_default)
	if coSpace_regenerateSecret == "1":
		coSpace_regenerateSecret = "true"
	elif coSpace_regenerateSecret == "2":
		coSpace_regenerateSecret = "false"
	else :
		coSpace_regenerateSecret = ""
	coSpace_parameters_list.append(coSpace_regenerateSecret)

	print("Conference - Recording Mode?")
	callProfile_recordingMode = input(menu_callProfile_recordingMode)
	if callProfile_recordingMode == "1":
		callProfile_recordingMode = "disabled"
	elif callProfile_recordingMode == "2":
		callProfile_recordingMode = "manual"
	elif callProfile_recordingMode == "3":
		callProfile_recordingMode = "automatic"
	else :
		callProfile_recordingMode = ""
	coSpace_parameters_list.append(callProfile_recordingMode)
	
	print("Conference - Streaming Mode?")
	callProfile_streamingMode = input(menu_callProfile_recordingMode)
	if callProfile_streamingMode == "1":
		callProfile_streamingMode = "disabled"
	elif callProfile_streamingMode == "2":
		callProfile_streamingMode = "manual"
	elif callProfile_streamingMode == "3":
		callProfile_streamingMode = "automatic"
	else :
		callProfile_streamingMode = ""
		coSpace_parameters_list.append(callProfile_streamingMode)

	if callProfile_streamingMode == "manual" or callProfile_streamingMode == "automatic":
		coSpace_streamUrl = ""
		while coSpace_streamUrl == "":
			coSpace_streamUrl = input("Stream URL (Mandatory): ")
		coSpace_parameters_list.append(coSpace_streamUrl)
	else:
		coSpace_streamUrl = ""
		coSpace_parameters_list.append(coSpace_streamUrl)

	print("Non-members and/or Guests are able to access to the Space?")
	coSpace_nonMemberAccess = input(menu_true_false)
	if coSpace_nonMemberAccess == "1":
		coSpace_nonMemberAccess = "true"
	elif coSpace_nonMemberAccess == "2":
		coSpace_nonMemberAccess = "false"
	else :
		coSpace_nonMemberAccess = ""
	coSpace_parameters_list.append(coSpace_nonMemberAccess)
	
	print("Conference - Locking/Unlocking, for Guests?")
	callProfile_locked = input(menu_true_false)
	if callProfile_locked == "1":
		callProfile_locked = "true"
	elif callProfile_locked == "2":
		callProfile_locked = "false"
	else :
		callProfile_locked = ""
	coSpace_parameters_list.append(callProfile_locked)

	if callProfile_locked != "false":
		print("Participant - can lock the Conference?")
		callLegProfile_callLockAllowed = input(menu_true_false)
		if callLegProfile_callLockAllowed == "1":
			callLegProfile_callLockAllowed = "true"
		elif callLegProfile_callLockAllowed == "2":
			callLegProfile_callLockAllowed = "false"
		else :
			callLegProfile_callLockAllowed = ""
		coSpace_parameters_list.append(callLegProfile_callLockAllowed)
	else:
		callLegProfile_callLockAllowed = ""
		coSpace_parameters_list.append(callLegProfile_callLockAllowed)
	
	print("Participant - Action for 'needsActivation' call legs when the last 'activator' leaves?")
	callLegProfile_deactivationMode = input(menu_callLegProfile_deactivationMode)
	if callLegProfile_deactivationMode == "1":
		callLegProfile_deactivationMode = "deactivate"
	elif callLegProfile_deactivationMode == "2":
		callLegProfile_deactivationMode = "disconnect"
	elif callLegProfile_deactivationMode == "3":
		callLegProfile_deactivationMode = "remainActivated"
	else :
		callLegProfile_deactivationMode = ""
	coSpace_parameters_list.append(callLegProfile_deactivationMode)

	if callLegProfile_deactivationMode == "deactivate":
		callLegProfile_deactivationModeTime = ""
		callLegProfile_deactivationModeTime = input("Number of seconds after the last 'activator' \
leaves before which the deactivationMode action is taken?\n")
		coSpace_parameters_list.append(callLegProfile_deactivationModeTime)
	else:
		callLegProfile_deactivationModeTime = ""
		coSpace_parameters_list.append(callLegProfile_deactivationModeTime)
	
	callLegProfile_joinToneParticipantThreshold = ""
	callLegProfile_joinToneParticipantThreshold = input("Participant - Number of participants up to \
which a 'join tone' will be played (0 disables this feature)?\n")
	coSpace_parameters_list.append(callLegProfile_joinToneParticipantThreshold)

	callLegProfile_leaveToneParticipantThreshold = ""
	callLegProfile_leaveToneParticipantThreshold = input("Participant - Number of participants up to \
which a 'leave tone' will be played (0 disables this feature)?\n")
	coSpace_parameters_list.append(callLegProfile_leaveToneParticipantThreshold)

	coSpace_tenant = input("Tenant ID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_tenant)

	coSpace_ownerJid = input("Space Owner's JID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_ownerJid)

	coSpace_ownerAdGuid = input("Space Owner's AD GUID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_ownerAdGuid)

	coSpace_meetingScheduler = input("Meeting Scheduler: ")
	coSpace_parameters_list.append(coSpace_meetingScheduler)
	
	coSpace_callId = input("Call ID: ")
	coSpace_parameters_list.append(coSpace_callId)

	if coSpace_callId == "":
		print("If no Call ID is specified, should new Call ID be created?")
		coSpace_requireCallId = input(menu_true_false)
		if coSpace_requireCallId == "1":
			coSpace_requireCallId = "true"
		elif coSpace_requireCallId == "2":
			coSpace_requireCallId = "false"
		else :
			coSpace_requireCallId = "false"
		coSpace_parameters_list.append(coSpace_requireCallId)
	else:
		coSpace_requireCallId = "false"
		coSpace_parameters_list.append(coSpace_requireCallId)

	coSpace_cdrTag = input("CDR Tag: ")
	coSpace_parameters_list.append(coSpace_cdrTag)

	print("Participant - Can end Call?")
	callLegProfile_endCallAllowed = input(menu_true_false)
	if callLegProfile_endCallAllowed == "1":
		callLegProfile_endCallAllowed = "true"
	elif callLegProfile_endCallAllowed == "2":
		callLegProfile_endCallAllowed = "false"
	else :
		callLegProfile_endCallAllowed = ""
	coSpace_parameters_list.append(callLegProfile_endCallAllowed)

	print("Participant - Can disconnect other participants?")
	callLegProfile_disconnectOthersAllowed = input(menu_true_false)
	if callLegProfile_disconnectOthersAllowed == "1":
		callLegProfile_disconnectOthersAllowed = "true"
	elif callLegProfile_disconnectOthersAllowed == "2":
		callLegProfile_disconnectOthersAllowed = "false"
	else :
		callLegProfile_disconnectOthersAllowed = ""
	coSpace_parameters_list.append(callLegProfile_disconnectOthersAllowed)

	print("Participant - is Audio-Only or Audio-Video?")
	callLegProfile_videoMode = input(menu_callLegProfiles_auto_disabled)
	if callLegProfile_videoMode == "1":
		callLegProfile_videoMode = "auto"
	elif callLegProfile_videoMode == "2":
		callLegProfile_videoMode = "disabled"
	else :
		callLegProfile_videoMode = ""
	coSpace_parameters_list.append(callLegProfile_videoMode)

	print("Participant - Participant cannot send Audio?")
	callLegProfile_txAudioMute = input(menu_true_false_default)
	if callLegProfile_txAudioMute == "1":
		callLegProfile_txAudioMute = "true"
	elif callLegProfile_txAudioMute == "2":
		callLegProfile_txAudioMute = "false"
	else :
		callLegProfile_txAudioMute = ""
	coSpace_parameters_list.append(callLegProfile_txAudioMute)

	print("Participant - Are allowed to audio mute self?")
	callLegProfile_muteSelfAllowed = input(menu_true_false)
	if callLegProfile_muteSelfAllowed == "1":
		callLegProfile_muteSelfAllowed = "true"
	elif callLegProfile_muteSelfAllowed == "2":
		callLegProfile_muteSelfAllowed = "false"
	else :
		callLegProfile_muteSelfAllowed = ""
	coSpace_parameters_list.append(callLegProfile_muteSelfAllowed)

	print("Participant - Can mute other participants?")
	callLegProfile_muteOthersAllowed = input(menu_true_false)
	if callLegProfile_muteOthersAllowed == "1":
		callLegProfile_muteOthersAllowed = "true"
	elif callLegProfile_muteOthersAllowed == "2":
		callLegProfile_muteOthersAllowed = "false"
	else :
		callLegProfile_muteOthersAllowed = ""
	coSpace_parameters_list.append(callLegProfile_muteOthersAllowed)

	callLegProfile_audioPacketSizeMs = ""
	callLegProfile_audioPacketSizeMs = input("Participant - Numeric value for preferred packet size (in milliseconds) for \
outgoing audio streams (default = 20ms)?\n")
	coSpace_parameters_list.append(callLegProfile_audioPacketSizeMs)

	print("Participant - Participant cannot send Video?")
	callLegProfile_txVideoMute = input(menu_true_false_default)
	if callLegProfile_txVideoMute == "1":
		callLegProfile_txVideoMute = "true"
	elif callLegProfile_txVideoMute == "2":
		callLegProfile_txVideoMute = "false"
	else :
		callLegProfile_txVideoMute = ""
	coSpace_parameters_list.append(callLegProfile_txVideoMute)

	print("Participant - Are allowed to Video mute self?")
	callLegProfile_videoMuteSelfAllowed = input(menu_true_false)
	if callLegProfile_videoMuteSelfAllowed == "1":
		callLegProfile_videoMuteSelfAllowed = "true"
	elif callLegProfile_videoMuteSelfAllowed == "2":
		callLegProfile_videoMuteSelfAllowed = "false"
	else :
		callLegProfile_videoMuteSelfAllowed = ""
	coSpace_parameters_list.append(callLegProfile_videoMuteSelfAllowed)

	print("Participant - Are allowed to Video mute others?")
	callLegProfile_videoMuteOthersAllowed = input(menu_true_false)
	if callLegProfile_videoMuteOthersAllowed == "1":
		callLegProfile_videoMuteOthersAllowed = "true"
	elif callLegProfile_videoMuteOthersAllowed == "2":
		callLegProfile_videoMuteOthersAllowed = "false"
	else :
		callLegProfile_videoMuteOthersAllowed = ""
	coSpace_parameters_list.append(callLegProfile_videoMuteOthersAllowed)

	print("Participant - SIP media encryption from Participant?")
	callLegProfile_sipMediaEncryption = input(menu_sipMediaEncryption)
	if callLegProfile_sipMediaEncryption == "1":
		callLegProfile_sipMediaEncryption = "optional"
	elif callLegProfile_sipMediaEncryption == "2":
		callLegProfile_sipMediaEncryption = "required"
	elif callLegProfile_sipMediaEncryption == "3":
		callLegProfile_sipMediaEncryption = "prohibited"
	else :
		callLegProfile_sipMediaEncryption = ""
	coSpace_parameters_list.append(callLegProfile_sipMediaEncryption)

	print("Participant - Participant can make TIP calls?")
	callLegProfile_telepresenceCallsAllowed = input(menu_true_false)
	if callLegProfile_telepresenceCallsAllowed == "1":
		callLegProfile_telepresenceCallsAllowed = "true"
	elif callLegProfile_telepresenceCallsAllowed == "2":
		callLegProfile_telepresenceCallsAllowed = "false"
	else :
		callLegProfile_telepresenceCallsAllowed = ""
	coSpace_parameters_list.append(callLegProfile_telepresenceCallsAllowed)

	# Following will accept parameters that can be created using callBrandingProfile
		# This section defines the behaviour of the conference customisation 
	print("Do you want to enable Branding?\n")
	branding = input(menu_true_false_default)

	if branding == "true":
		callBrandingProfile_invitationTemplate = ""
		callBrandingProfile_invitationTemplate = input("Conference Branding - Invitation Template URL?\n")
		coSpace_parameters_list.append(callBrandingProfile_invitationTemplate)

		callBrandingProfile_resourceLocation = ""
		callBrandingProfile_resourceLocation = input("Conference Branding - Branding Files Location URL?\n")
		coSpace_parameters_list.append(callBrandingProfile_resourceLocation)
	else:
		callBrandingProfile_invitationTemplate = ""
		coSpace_parameters_list.append(callBrandingProfile_invitationTemplate)
		callBrandingProfile_resourceLocation = ""
		coSpace_parameters_list.append(callBrandingProfile_resourceLocation)		

	space_coSpace_parameters_list ["coSpace_name"] = coSpace_name
	space_coSpace_parameters_list ["coSpace_uri"] = coSpace_uri
	if coSpace_passcode != "":
		space_coSpace_parameters_list ["coSpace_passcode"] = coSpace_passcode
	if coSpace_secret != "":
		space_coSpace_parameters_list ["coSpace_secret"] = coSpace_secret
	if coSpace_secondary_uri != "":
		space_coSpace_parameters_list ["coSpace_secondary_uri"] = coSpace_secondary_uri
	if coSpace_defaultLayout != "":
		space_coSpace_parameters_list ["coSpace_defaultLayout"] = coSpace_defaultLayout
	if coSpace_regenerateSecret != "":
		space_coSpace_parameters_list ["coSpace_regenerateSecret"] = coSpace_regenerateSecret
	if coSpace_streamUrl != "":
		space_coSpace_parameters_list ["coSpace_streamUrl"] = coSpace_streamUrl
	if coSpace_nonMemberAccess != "":
		space_coSpace_parameters_list ["coSpace_nonMemberAccess"] = coSpace_nonMemberAccess
	if coSpace_tenant != "":
		space_coSpace_parameters_list ["coSpace_tenant"] = coSpace_tenant
	if coSpace_ownerJid != "":
		space_coSpace_parameters_list ["coSpace_ownerJid"] = coSpace_ownerJid
	if coSpace_ownerAdGuid != "":
		space_coSpace_parameters_list ["coSpace_ownerAdGuid"] = coSpace_ownerAdGuid
	if coSpace_meetingScheduler != "":
		space_coSpace_parameters_list ["coSpace_meetingScheduler"] = coSpace_meetingScheduler
	if coSpace_callId != "":
		space_coSpace_parameters_list ["coSpace_callId"] = coSpace_callId
	if coSpace_requireCallId != "":
		space_coSpace_parameters_list ["coSpace_requireCallId"] = coSpace_requireCallId
	if coSpace_cdrTag != "":
		space_coSpace_parameters_list ["coSpace_cdrTag"] = coSpace_cdrTag

	if callProfile_participantLimit != "":
		space_coSpace_callProfile_parameters_list ["callProfile_participantLimit"] = callProfile_participantLimit
	if callProfile_messageBoardEnabled != "":
		space_coSpace_callProfile_parameters_list ["callProfile_messageBoardEnabled"] = callProfile_messageBoardEnabled
	if callProfile_passcodeMode != "":
		space_coSpace_callProfile_parameters_list ["callProfile_passcodeMode"] = callProfile_passcodeMode
	if callProfile_passcodeTimeout != "":
		space_coSpace_callProfile_parameters_list ["callProfile_passcodeTimeout"] = callProfile_passcodeTimeout
	if callProfile_recordingMode != "":
		space_coSpace_callProfile_parameters_list ["callProfile_recordingMode"] = callProfile_recordingMode
	if callProfile_streamingMode != "":
		space_coSpace_callProfile_parameters_list ["callProfile_streamingMode"] = callProfile_streamingMode
	if callProfile_locked != "":
		space_coSpace_callProfile_parameters_list ["callProfile_locked"] = callProfile_locked

	if callLegProfile_maxCallDurationTime != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_maxCallDurationTime"] = callLegProfile_maxCallDurationTime
	if callLegProfile_participantCounter != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_participantCounter"] = callLegProfile_participantCounter
	if callLegProfile_changeLayoutAllowed != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_changeLayoutAllowed"] = callLegProfile_changeLayoutAllowed
	if callLegProfile_participantLabels != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_participantLabels"] = callLegProfile_participantLabels
	if callLegProfile_qualityMain != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_qualityMain"] = callLegProfile_qualityMain
	if callLegProfile_presentationContributionAllowed != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_presentationContributionAllowed"] = callLegProfile_presentationContributionAllowed
	if callLegProfile_qualityPresentation != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_qualityPresentation"] = callLegProfile_qualityPresentation
	if callLegProfile_presentationDisplayMode != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_presentationDisplayMode"] = callLegProfile_presentationDisplayMode
	if callLegProfile_sipPresentationChannelEnabled != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_sipPresentationChannelEnabled"] = callLegProfile_sipPresentationChannelEnabled
	if callLegProfile_bfcpMode != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_bfcpMode"] = callLegProfile_bfcpMode
	if callLegProfile_callLockAllowed != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_callLockAllowed"] = callLegProfile_callLockAllowed
	if callLegProfile_deactivationMode != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_deactivationMode"] = callLegProfile_deactivationMode
	if callLegProfile_deactivationModeTime != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_deactivationModeTime"] = callLegProfile_deactivationModeTime
	if callLegProfile_joinToneParticipantThreshold != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_joinToneParticipantThreshold"] = callLegProfile_joinToneParticipantThreshold
	if callLegProfile_leaveToneParticipantThreshold != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_leaveToneParticipantThreshold"] = callLegProfile_leaveToneParticipantThreshold
	if callLegProfile_endCallAllowed != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_endCallAllowed"] = callLegProfile_endCallAllowed
	if callLegProfile_disconnectOthersAllowed != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_disconnectOthersAllowed"] = callLegProfile_disconnectOthersAllowed
	if callLegProfile_videoMode != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_videoMode"] = callLegProfile_videoMode
	if callLegProfile_txAudioMute != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_txAudioMute"] = callLegProfile_txAudioMute
	if callLegProfile_muteSelfAllowed != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_muteSelfAllowed"] = callLegProfile_muteSelfAllowed
	if callLegProfile_muteOthersAllowed != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_muteOthersAllowed"] = callLegProfile_muteOthersAllowed
	if callLegProfile_audioPacketSizeMs != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_audioPacketSizeMs"] = callLegProfile_audioPacketSizeMs
	if callLegProfile_txVideoMute != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_txVideoMute"] = callLegProfile_txVideoMute
	if callLegProfile_videoMuteSelfAllowed != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_videoMuteSelfAllowed"] = callLegProfile_videoMuteSelfAllowed
	if callLegProfile_videoMuteOthersAllowed != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_videoMuteOthersAllowed"] = callLegProfile_videoMuteOthersAllowed
	if callLegProfile_sipMediaEncryption != "":
		space_coSpace_callLegProfile_parameters_list ["callLegProfile_sipMediaEncryption"] = callLegProfile_sipMediaEncryption
	if callLegProfile_telepresenceCallsAllowed != "":
		space_coSpace_callLegProfile_parameters_list \
		["callLegProfile_telepresenceCallsAllowed"] = callLegProfile_telepresenceCallsAllowed

	if callBrandingProfile_invitationTemplate != "":
		space_coSpace_callBrandingProfile_parameters_list \
		["callBrandingProfile_invitationTemplate"] = callBrandingProfile_invitationTemplate
	if callBrandingProfile_resourceLocation != "":
		space_coSpace_callBrandingProfile_parameters_list \
		["callBrandingProfile_resourceLocation"] = callBrandingProfile_resourceLocation

	return coSpace_parameters_list

def list_for_space_modification(coSpace_parameters_list):
	coSpace_name = input("Name: ")
	coSpace_parameters_list.append(coSpace_name)

	coSpace_uri = input("URI: ")
	coSpace_parameters_list.append(coSpace_uri)

	coSpace_secondary_uri = input("Secondary URI: ")
	coSpace_parameters_list.append(coSpace_secondary_uri)

	coSpace_defaultLayout = input(menu_defaultLayout)
	if coSpace_defaultLayout == "1":
		coSpace_defaultLayout = "allEqual"
	elif coSpace_defaultLayout == "2":
		coSpace_defaultLayout = "speakerOnly"
	elif coSpace_defaultLayout == "3":
		coSpace_defaultLayout = "telepresence"
	elif coSpace_defaultLayout == "4":
		coSpace_defaultLayout = "stacked"
	elif coSpace_defaultLayout == "5":
		coSpace_defaultLayout = "allEqualQuarters"
	elif coSpace_defaultLayout == "6":
		coSpace_defaultLayout = "allEqualNinths"
	elif coSpace_defaultLayout == "7":
		coSpace_defaultLayout = "allEqualSixteenths"
	elif coSpace_defaultLayout == "8":
		coSpace_defaultLayout = "allEqualTwentyFifths"
	elif coSpace_defaultLayout == "9":
		coSpace_defaultLayout = "onePlusFive"
	elif coSpace_defaultLayout == "10":
		coSpace_defaultLayout = "onePlusSeven"
	elif coSpace_defaultLayout == "11":
		coSpace_defaultLayout = "onePlusNine"
	elif coSpace_defaultLayout == "12":
		coSpace_defaultLayout = "automatic"
	elif coSpace_defaultLayout == "13":
		coSpace_defaultLayout = "onePlusN"
	else :
		coSpace_defaultLayout = ""
	coSpace_parameters_list.append(coSpace_defaultLayout)

	coSpace_passcode = input("Passcode to join this Space: ")
	coSpace_parameters_list.append(coSpace_passcode)

	print("Non-members and/or Guests are able to access to the Space?")
	coSpace_nonMemberAccess = input(menu_true_false)
	if coSpace_nonMemberAccess == "1":
		coSpace_nonMemberAccess = "true"
	elif coSpace_nonMemberAccess == "2":
		coSpace_nonMemberAccess = "false"
	else :
		coSpace_nonMemberAccess = ""
	coSpace_parameters_list.append(coSpace_nonMemberAccess)
	
	coSpace_tenant = input("Tenant ID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_tenant)

	coSpace_ownerJid = input("Space Owner's JID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_ownerJid)

	coSpace_ownerAdGuid = input("Space Owner's AD GUID (Values entered in wrong format wont be updated): ")
	coSpace_parameters_list.append(coSpace_ownerAdGuid)

	coSpace_meetingScheduler = input("Meeting Scheduler: ")
	coSpace_parameters_list.append(coSpace_meetingScheduler)
	
	coSpace_callId = input("Call ID: ")
	coSpace_parameters_list.append(coSpace_callId)

	if coSpace_callId == "":
		print("If no Call ID is specified, should new Call ID be created?")
		coSpace_requireCallId = input(menu_true_false)
		if coSpace_requireCallId == "1":
			coSpace_requireCallId = "true"
		elif coSpace_requireCallId == "2":
			coSpace_requireCallId = "false"
		else :
			coSpace_requireCallId = "false"
		coSpace_parameters_list.append(coSpace_requireCallId)
	else:
		coSpace_requireCallId = "false"
		coSpace_parameters_list.append(coSpace_requireCallId)

	coSpace_cdrTag = input("CDR Tag: ")
	coSpace_parameters_list.append(coSpace_cdrTag)

	if coSpace_name != "":
		space_coSpace_parameters_list ["coSpace_name"] = coSpace_name
	if coSpace_uri != "":
		space_coSpace_parameters_list ["coSpace_uri"] = coSpace_uri
	if coSpace_passcode != "":
		space_coSpace_parameters_list ["coSpace_passcode"] = coSpace_passcode
	#space_coSpace_parameters_list ["coSpace_secret"] = coSpace_secret
	if coSpace_secondary_uri != "":
		space_coSpace_parameters_list ["coSpace_secondary_uri"] = coSpace_secondary_uri
	if coSpace_defaultLayout != "":
		space_coSpace_parameters_list ["coSpace_defaultLayout"] = coSpace_defaultLayout
	#space_coSpace_parameters_list ["coSpace_regenerateSecret"] = coSpace_regenerateSecret
	#space_coSpace_parameters_list ["coSpace_streamUrl"] = coSpace_streamUrl
	if coSpace_nonMemberAccess != "":
		space_coSpace_parameters_list ["coSpace_nonMemberAccess"] = coSpace_nonMemberAccess
	if coSpace_tenant != "":
		space_coSpace_parameters_list ["coSpace_tenant"] = coSpace_tenant
	if coSpace_ownerJid != "":
		space_coSpace_parameters_list ["coSpace_ownerJid"] = coSpace_ownerJid
	if coSpace_ownerAdGuid != "":
		space_coSpace_parameters_list ["coSpace_ownerAdGuid"] = coSpace_ownerAdGuid
	if coSpace_meetingScheduler != "":
		space_coSpace_parameters_list ["coSpace_meetingScheduler"] = coSpace_meetingScheduler
	if coSpace_callId != "":
		space_coSpace_parameters_list ["coSpace_callId"] = coSpace_callId
	if coSpace_requireCallId != "":
		space_coSpace_parameters_list ["coSpace_requireCallId"] = coSpace_requireCallId
	if coSpace_cdrTag != "":
		space_coSpace_parameters_list ["coSpace_cdrTag"] = coSpace_cdrTag

	return coSpace_parameters_list

def get_coSpace_parameters_from_list():
	return space_coSpace_parameters_list

def get_coSpace_callProfile_parameters_from_list():
	return space_coSpace_callProfile_parameters_list

def get_coSpace_callLegProfile_parameters_from_list():
	return space_coSpace_callLegProfile_parameters_list

def get_coSpace_callBrandingProfile_parameters_from_list():
	return space_coSpace_callBrandingProfile_parameters_list

# Finds number of objects from GET API output.
def get_number_of_objects(request_handle, cms_objects):
	get = request_handle.text
	get = get.replace("<?","\n\n<?")
	get = get.replace("><"," ")
	get = get.replace ("<","")
	get = get.replace (">","")
	list1 = get.split(" ")
	length=len(list1)
	for x in range(0,length):
		if list1[x]==cms_objects:
			value = list1[x+1]
			value = value.replace("total=","")
			value = value.replace('"','')
			return int(value)
			break

# Finds number of objects from GET API output.
def get_number_of_objects_new(request_handle_text, cms_objects):
	get = request_handle_text
	get = get.replace("<?","\n\n<?")
	get = get.replace("><"," ")
	get = get.replace ("<","")
	get = get.replace (">","")
	list1 = get.split(" ")
	length=len(list1)
	for x in range(0,length):
		if list1[x]==cms_objects:
			value = list1[x+1]
			value = value.replace("total=","")
			value = value.replace('"','')
			return int(value)
			break

# find the space id of the 1st object listed.
# This function will return 1 object id out of all the object ids.
# This function will filter 1 output at a time. 
def get_object_id(cms_objects, number_of_objects, offset_value, cms_ip, cms_webadmin_port, cms_webadmin_authorization, \
	cms_webadmin_content_type, cms_login, cms_password):
	if number_of_objects == 1:
		cms_object_filter = cms_objects
	else:
		cms_object_filter = (cms_objects+"?limit=1&offset="+str(offset_value))
	cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_object_filter
	r = api_get(cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
	get = r.text
	get = get.replace("<?","\n\n<?")
	get = get.replace("><"," ")
	get = get.replace ("<","")
	get = get.replace (">","")
	list1 = get.split(" ")
	length=len(list1)
	for x in range(1,length):
		if list1[x]==cms_objects[:-1]:
			value = list1[x+1]
			value = value.replace("id=","")
			value = value.replace('"','')
			return value
			break

# This function will create a list of all the object ids in a GET command.
# This function will use a loop to get object ids one by one using the previous function. 
def get_object_id_list(cms_objects, cms_ip, number_of_objects, cms_webadmin_port, cms_webadmin_authorization, \
		cms_webadmin_content_type, cms_login, cms_password):
	object_list = []
	if number_of_objects == 0:
		print("There are no objects created")
	else:
		for i in range(0,int(number_of_objects)):
			object_id = get_object_id(cms_objects, number_of_objects, i, cms_ip, cms_webadmin_port, \
				cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
			object_list.append(object_id)
	return object_list

# Compares the GETs before and after POST and finds the newly created object ID. 
def find_new_object_from_two_objectLists(list1, list2):
	list1_length = len(list1)
	list2_length = len(list2)

	if list1_length == 0:
		pass
		return list2[0]
	else:
		for x in range(0,list2_length):
			match = 1
			for y in range(0,list1_length):
				if list2[x] == list1[y]:
					match = 1
					break
				else:
					match = 0
			if match == 0:
				return list2[x]

# Creates new object.
def create_new_object(cms_objects, cms_ip, cms_webadmin_port, cms_webadmin_authorization, cms_webadmin_content_type, \
	cms_login, cms_password):
	print("  Info - Creating new ",cms_objects[:-1],".")
	cms_url = "https://" + cms_ip + ":" + cms_webadmin_port + "/api/v1/" + cms_objects
	get = api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
	number_of_objects = get_number_of_objects (get, cms_objects)
	list_before = get_object_id_list (cms_objects, cms_ip, number_of_objects, cms_webadmin_port, cms_webadmin_authorization, \
		cms_webadmin_content_type, cms_login, cms_password)
	post = api_post (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
	get = api_get (cms_url, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, cms_password)
	number_of_objects = get_number_of_objects (get, cms_objects)
	list_after = get_object_id_list (cms_objects, cms_ip, number_of_objects, cms_webadmin_port, cms_webadmin_authorization, \
		cms_webadmin_content_type, cms_login, cms_password)
	new_id = find_new_object_from_two_objectLists (list_before, list_after)
	print("  Info - Created new ",cms_objects[:-1],".")
	return new_id

# Returns nothing.
# Input - dictionary of all the object parameters.
# Input - object id. 
def put_fields(object_parameters_dictionary, cms_object, cms_url, object_id, cms_webadmin_authorization, \
	cms_webadmin_content_type, cms_login, cms_password):
	object_parameters_keys = list(object_parameters_dictionary.keys())
	object_parameters_list = []
	dic_temp = {}
	for i in range(0,len(object_parameters_keys)):
		key = object_parameters_keys[i]
		cms_object_ = cms_object+"_"
		key1 = key.replace(cms_object_, "")
		dic_temp = {key1: object_parameters_dictionary[object_parameters_keys[i]]}
		r = api_put(cms_url, object_id, dic_temp, cms_webadmin_authorization, cms_webadmin_content_type, cms_login, \
			cms_password)
		dic_temp = {}

# Inputs single object r.text (r = get handler) and the parameter whose value has to be returned.
# Returns the value of the parameter mentioned above.
def get_parameter_from_1_get(request_handle_text, parameter):
	parameter_value = request_handle_text
	#cms_object = cms_objects[:-1]
	parameter_value = parameter_value.replace("<","\n")
	list1 = parameter_value.split("\n")
	length = len(list1)
	len_parameter = len(parameter)
	value = "None"	# Initializing the varialble if the function doesnt find any values. 
	for i in range(0,length):
		text = list1[i]
		if text[0:len_parameter] == parameter:
			value = text[len_parameter+1:]
			break
	value = value.replace('"','')
	value = value.replace(">", "")
	return value

# Inputs single object r.text (r = get handler) and the parameter whose value has to be returned.
# Can only find a value if it is in this format, <type>acano</type>
# Returns the value of the parameter mentioned above.
def get_parameter_from_1_callLeg(request_handle_text, parameter):
	parameter_value = request_handle_text
	parameter_value = parameter_value.replace("><",">\n<")
	list1 = parameter_value.split("\n")
	length = len(list1)
	len_parameter = len(parameter)
	for i in range(0,length):
		text = list1[i]
		if text[0:len_parameter] == parameter:
			value = text[len_parameter:]
			break
	parameter = parameter[0]+"/"+parameter[1:]
	value = value.replace(parameter,"")
	return value














































# In-Progress Functions

def print_output_to_file(text, file_name):	# working on it
	f = open(file_name, "w")
	f.write(text)













