from asyncio import events
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import re
import requests
from datetime import datetime
import json

with open('resource/district_lookup.json', 'r') as f:
    print("🔍 Loading district codes from JSON file..." )
    DISTRICT_CODE_MAP = json.load(f)

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import re # Import regex for validation

class ActionInformNumberSlotFilling(Action):
    def name(self) -> Text:
        return "action_inform_number_slot_filling"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        events = []

        # --- Validate and fill phone_number ---
        phone_number = next(tracker.get_latest_entity_values("phone_number"), None)
        if phone_number:
            # Basic validation for phone number (e.g., Nepal's 10-digit mobile)
            # Adjust regex based on your specific validation rules
            if re.fullmatch(r'^\d{10}$', phone_number): # Checks for exactly 10 digits
                dispatcher.utter_message(f"Okay, I've noted your phone number as {phone_number}.")
                events.append(SlotSet("phone_number", phone_number))
                events.append(FollowupAction("send_phone_number_to_backend"))
            else:
                dispatcher.utter_message(
                    f"That doesn't look like a valid 10-digit phone number. Could you please provide a valid one?"
                )
                events.append(SlotSet("phone_number", None)) # Clear invalid slot

        # --- Validate and fill mpin ---
        mpin = next(tracker.get_latest_entity_values("mpin"), None)
        if mpin:
            # Basic validation for MPIN (e.g., 6 digits)
            if re.fullmatch(r'^\d{6}$', mpin): # Checks for exactly 6 digits
                dispatcher.utter_message(f"Your MPIN has been noted.")
                events.append(SlotSet("mpin", mpin))
                events.append(FollowupAction("send_mpin_to_backend"))
            else:
                dispatcher.utter_message(
                    f"The MPIN should be a 6-digit number. Please provide a valid MPIN."
                )
                events.append(SlotSet("mpin", None)) # Clear invalid slot
        else:
            return []
        return events

# this action request for phone number and sendt it to the backend
class ActionRequestPhoneNumber(Action):
    def name(self) -> Text:
        return "send_phone_number_to_backend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Request phone number from the user
        slot_value = tracker.get_slot("phone_number")

        if slot_value:
            phone_regex = r'^\d{10}$'  # Regex for a 10-digit phone number
            if not re.match(phone_regex, slot_value):
                dispatcher.utter_message(text="Please provide a valid 10-digit phone number.")
                return [SlotSet("phone_number", None)]

            try:
                response = requests.post(
                    "http://localhost:5001/api/phone-number",
                    json={"phone_number": slot_value},
                    timeout=10
                )
                if response.status_code == 200:
                    dispatcher.utter_message(text=f"📞 Phone number received successfully! Please provide the MPIN number received on the {slot_value}.")
                    events.append(FollowupAction("utter_ask_mpin"))
                else:
                    dispatcher.utter_message(text="❌ Failed to send phone number. Please try again later.")
            except requests.Timeout:
                dispatcher.utter_message(text="⏳ Request timed out. Please try again later.")
            except requests.RequestException as e:
                dispatcher.utter_message(text="❌ An error occurred. Please try again later.")
            return [SlotSet("phone_number", slot_value)]
        else:
            dispatcher.utter_message(text="📞 Please provide your phone number to proceed with the driving license application.")
        
        return []
    
class ActionPassMpin(Action):
    def name(self) -> Text:
        return "send_mpin_to_backend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mpin = tracker.get_slot("mpin")
        if not mpin:
            dispatcher.utter_message(text="Please provide your MPIN to proceed.")
            return []

        # Validate MPIN format
        if not re.match(r'^\d{6}$', mpin):
            dispatcher.utter_message(text="MPIN must be a 6-digit number. Please try again.")
            return []

        try:
            response = requests.post(
                "http://localhost:5001/api/mpin",
                json={"mpin": mpin},
                timeout=10
            )
            if response.status_code == 200:
                dispatcher.utter_message(text="✅ MPIN accepted! You can now proceed with the driving license application.")
                # Optionally, you can clear the MPIN slot after successful validation
                return [SlotSet("mpin", mpin), FollowupAction("driving_license_form")]
            else:
                dispatcher.utter_message(text="❌ Invalid MPIN. Please check and try again.")
        except requests.Timeout:
            dispatcher.utter_message(text="⏳ Request timed out. Please try again later.")
        except requests.RequestException as e:
            dispatcher.utter_message(text="❌ An error occurred while validating the MPIN. Please try again later.")

        return []

class ValidateDrivingLicenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_driving_license_form"
    
    def validate(
    self,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate only the currently requested slot."""
        
        requested_slot = tracker.get_slot('requested_slot')
        slot_value = tracker.get_slot(requested_slot)
        
        print(f"🎯 VALIDATING ONLY: {requested_slot} = {slot_value}")
        
        # Call the specific validator based on requested slot
        if requested_slot == 'firstname':
            return self.validate_firstname(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'middlename':
            return self.validate_middlename(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'lastname':
            return self.validate_lastname(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'email':
            return self.validate_email(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'citizenshipno':
            return self.validate_citizenshipno(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'addresstype':
            return self.validate_addresstype(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'issuedistrict':
            return self.validate_issuedistrict(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'dob':
            return self.validate_dob(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'issuedate':
            return self.validate_issuedate(slot_value, dispatcher, tracker, domain)
        elif requested_slot == 'citizenship_number':
            return self.validate_citizenship_number(slot_value, dispatcher, tracker, domain)
        return {requested_slot: slot_value}

    def validate_firstname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate firstname value."""
        if len(slot_value) < 2:
            dispatcher.utter_message(text="First name must be at least 2 characters long.")
            return {"firstname": None}
        return {"firstname": slot_value}

    def validate_lastname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate lastname value."""
        if len(slot_value) < 2:
            dispatcher.utter_message(text="Last name must be at least 2 characters long.")
            return {"lastname": None}
        return {"lastname": slot_value}

    def validate_dob(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate date of birth."""
        try:
            date_obj = datetime.strptime(slot_value, "%Y-%m-%d")
            
            # Check if the date is in the future
            today = datetime.now()
            if date_obj > today:
                dispatcher.utter_message(text="Date of birth cannot be in the future. Please provide a valid date.")
                return {"dob": None}
            
            # Calculate age more reliably
            age = today.year - date_obj.year
            if today.month < date_obj.month or (today.month == date_obj.month and today.day < date_obj.day):
                age -= 1
                
            if age < 16:
                dispatcher.utter_message(text="You must be at least 16 years old to apply for a driving license.")
                return {"dob": None}
                
            return {"dob": slot_value}
            
        except ValueError:
            dispatcher.utter_message(text="Please provide date in YYYY-MM-DD format (e.g., 1990-05-15).")
            return {"dob": None}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email address."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, slot_value):
            dispatcher.utter_message(text="Please provide a valid email address.")
            return {"email": None}
        return {"email": slot_value}

    def validate_citizenshipno(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate citizenship number."""
        if not slot_value.isdigit() or len(slot_value) < 8:
            dispatcher.utter_message(text="Citizenship number should be at least 8 digits.")
            return {"citizenshipno": None}
        return {"citizenshipno": slot_value}

    def validate_addresstype(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate address type."""
        valid_types = ["permanent", "temporary"]
        if slot_value.lower() not in valid_types:
            dispatcher.utter_message(text="Address type must be either 'permanent' or 'temporary'.")
            return {"addresstype": None}
        return {"addresstype": slot_value.lower()}

    def validate_issuedate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate issue date."""
        try:
            date_obj = datetime.strptime(slot_value, "%Y-%m-%d")
            # Check if date is not in the past
            if date_obj.date() < datetime.now().date():
                dispatcher.utter_message(text="Issue date cannot be in the past.")
                return {"issuedate": None}
            return {"issuedate": slot_value}
        except ValueError:
            dispatcher.utter_message(text="Please provide date in YYYY-MM-DD format (e.g., 2024-06-15).")
            return {"issuedate": None}
            
    def validate_issuedistrict(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> Dict[str, Any]:
        code = DISTRICT_CODE_MAP.get(slot_value, "00")
        return {"issuedistrict": slot_value, "issuedistrict_code": code}
    

# This action sets the district code based on the district name provided by the user. 
class ActionSetDistrictCode(Action):
    def name(self) -> str:
        return "action_set_issuedistrict_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        district = tracker.get_slot("issuedistrict")
        code = DISTRICT_CODE_MAP.get(district, "00")  # Default to 00 if not found

        return [SlotSet("issuedistrict_code", code)]


class ActionSubmitDrivingLicense(Action):
    def name(self) -> Text:
        return "action_submit_driving_license"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Collect all form data
        application_data = {
            "phone_number": tracker.get_slot("phone_number"),
            "firstname": tracker.get_slot("firstname"),
            "middlename": tracker.get_slot("middlename"),
            "lastname": tracker.get_slot("lastname"),
            "dob": tracker.get_slot("dob"),
            "citizenshipno": tracker.get_slot("citizenshipno"),
            "addresstype": tracker.get_slot("addresstype"),
            "issuedistrict": tracker.get_slot("issuedistrict"),
            "issuedistrict_code": tracker.get_slot("issuedistrict_code"),
            "issuedate": tracker.get_slot("issuedate"),
            "email": tracker.get_slot("email")
        }

        try:
            response = requests.post(
                "http://localhost:5001/api/driving-license",
                json=application_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                dispatcher.utter_message(
                    text=f"✅ Great! Your driving license application has been submitted successfully!\n"
                         f"📋 Application ID: {result.get('application_id')}\n"
                         f"📧 Confirmation sent to: {application_data['email']}\n"
                         f"⏱️ Processing time: 5-7 business days"
                )
            else:
                dispatcher.utter_message(
                    text="❌ Sorry, there was an issue submitting your application. Please try again later."
                )
        except requests.exceptions.RequestException:
            dispatcher.utter_message(
                text="⚠️ Unable to connect to the application service. Your data has been saved and will be processed manually."
            )

        # Clear all form slots after submission
        return [
            {"event": "slot", "name": "document_type", "value": None},
            {"event": "slot", "name": "phone_number", "value": None},
            {"event": "slot", "name": "mpin", "value": None},
            {"event": "slot", "name": "firstname", "value": None},
            {"event": "slot", "name": "middlename", "value": None},
            {"event": "slot", "name": "lastname", "value": None},
            {"event": "slot", "name": "dob", "value": None},
            {"event": "slot", "name": "citizenshipno", "value": None},
            {"event": "slot", "name": "addresstype", "value": None},
            {"event": "slot", "name": "issuedistrict", "value": None},
            {"event": "slot", "name": "issuedistrict_code", "value": None},
            {"event": "slot", "name": "issuedate", "value": None},
            {"event": "slot", "name": "email", "value": None},
        ]


class ActionResetForm(Action):
    def name(self) -> Text:
        return "action_reset_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="🔄 Starting fresh! Previous data has been cleared.")
        
        return [
            {"event": "slot", "name": "phone_number", "value": None},
            {"event": "slot", "name": "mpin", "value": None},
            {"event": "slot", "name": "firstname", "value": None},
            {"event": "slot", "name": "middlename", "value": None},
            {"event": "slot", "name": "lastname", "value": None},
            {"event": "slot", "name": "dob", "value": None},
            {"event": "slot", "name": "citizenshipno", "value": None},
            {"event": "slot", "name": "addresstype", "value": None},
            {"event": "slot", "name": "issuedistrict", "value": None},
            {"event": "slot", "name": "issuedistrict_code", "value": None},
            {"event": "slot", "name": "issuedate", "value": None},
            {"event": "slot", "name": "email", "value": None},
        ]