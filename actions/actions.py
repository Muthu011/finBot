# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCalculateTakeHomeSalary(Action):

    def name(self):
        return "action_calculate_take_home_salary"

    def run(self, dispatcher, tracker: Tracker, domain):
        age = tracker.get_slot('age')
        basic_salary = tracker.get_slot('basic_salary')
        hra = tracker.get_slot('hra')
        other_allowances = tracker.get_slot('other_allowances')
        deductions = tracker.get_slot('deductions')
        investment = tracker.get_slot('investment')
        city = tracker.get_slot('city')

        if not all([age, basic_salary, hra, other_allowances, deductions, investment, city]):
            dispatcher.utter_message(text="Please provide all the required details to calculate your take-home salary.")
            return []

        print('  1 ',age)
        print('  2 ',basic_salary)
        print('  3 ',hra)
        print('  4 ',other_allowances)
        print('  5 ',deductions)
        print('  6 ',investment)
        print('  7 ',city)

        try:

            # Calculate gross salary
            gross_salary = float(basic_salary) + float(hra)  + float(other_allowances) 

            # Calculate taxable income
            taxable_income =float(gross_salary)  - float(deductions)  - float(investment)
            tax = self.calculate_tax(taxable_income, float(age))

            # Calculate tax based on Indian tax regime (simplified)
            # if taxable_income <= 250000:
            #     tax = 0
            # elif taxable_income <= 500000:
            #     tax = (taxable_income - 250000) * 0.05
            # elif taxable_income <= 1000000:
            #     tax = 12500 + (taxable_income - 500000) * 0.2
            # else:
            #     tax = 112500 + (taxable_income - 1000000) * 0.3

            # Calculate take-home salary
            take_home_salary =float(gross_salary)  -float(tax) 

            dispatcher.utter_message(text=f"Based on the details provided, your take-home salary is {take_home_salary:.2f}.")
        except (TypeError, ValueError) as e:
            print('  err ',TypeError)
            print('  err ',ValueError)
            print('  error ',e)

            # Handle error if conversion fails or if values are not numeric
            dispatcher.utter_message(text="Oops! An error occurred while calculating your salary. Please make sure the provided details are numeric. }")
            return []
    
        return []

    def calculate_tax(self, income, age):
        # Tax calculation logic as per Indian tax regime (simplified example)
        tax = 0
        if age < 60:
            if income <= 250000:
                tax = 0
            elif income <= 500000:
                tax = (income - 250000) * 0.05
            elif income <= 1000000:
                tax = (income - 500000) * 0.2 + 12500
            else:
                tax = (income - 1000000) * 0.3 + 112500
        elif age < 80:
            if income <= 300000:
                tax = 0
            elif income <= 500000:
                tax = (income - 300000) * 0.05
            elif income <= 1000000:
                tax = (income - 500000) * 0.2 + 10000
            else:
                tax = (income - 1000000) * 0.3 + 110000
        else:
            if income <= 500000:
                tax = 0
            elif income <= 1000000:
                tax = (income - 500000) * 0.2
            else:
                tax = (income - 1000000) * 0.3 + 100000

        return tax