# Credit Calculator
# Author: Jason Tolbert (http://github.com/jasonalantolbert)
# Python Version: 3.6


# BEGINNING OF PROGRAM


# import statements


import argparse
import sys
import math
import re


# entry point functions


def type_annuity(annuity, principal, periods, interest):

    # these conditional statements determine which parameter
    # the user left empty and returns the output of the function that calculates
    # the corresponding value

    if periods is None:
        annuity = int(annuity)
        principal = int(principal)
        interest = float(interest) / (12 * 100)
        return calculate_periods(principal, annuity, interest)

    if annuity is None:
        principal = int(principal)
        periods = int(periods)
        interest = float(interest) / (12 * 100)
        return calculate_annuity(principal, periods, interest)

    if principal is None:
        annuity = int(annuity)
        periods = int(periods)
        interest = float(interest) / (12 * 100)
        return calculate_principal(annuity, periods, interest)


def type_diff(payment, principal, periods, interest):

    # this function first checks that the user did NOT input a value for
    # the payment parameter and returns the output of the the differentiated payments calculation
    # function if that check returns true

    if payment is not None:
        return "Invalid parameters"
    else:
        principal = int(principal)
        periods = int(periods)
        interest = float(interest) / (12 * 100)
        return calculate_diff(principal, periods, interest)


# calculation functions


def calculate_periods(principal, annuity, interest):
    periods = math.ceil(math.log(annuity / (annuity - interest * principal), 1 + interest))

    if (annuity * periods) > principal:  # adds overpayment to the output if applicable
        if periods % 12 == 0:  # if the time period is number of years is a multiple of 12
            return f"It will take {periods // 12} years to repay this credit!\n" \
                   f"Overpayment = {(annuity * periods) - principal}"
        elif periods < 12:  # if the time period is less than a year
            return f"It will take {periods} {'month' if periods == 1 else 'months'} to repay this credit!\n" \
                   f"Overpayment = {(annuity * periods) - principal}"
        else:  # if the time period is more than one year + less than 12 additional months
            return f"It will take {periods // 12} years and {periods % 12} months to repay this credit!\n" \
                   f"Overpayment = {(annuity * periods) - principal}"
    else:  # runs if there is no overpayment
        if periods % 12 == 0:  # if the time period is number of years is a multiple of 12
            return f"It will take {periods // 12} years to repay this credit!"
        elif periods < 12:  # if the time period is less than a year
            return f"It will take {periods} {'month' if periods == 1 else 'months'} to repay this credit!"
        else:  # if the time period is more than one year + less than 12 additional months
            return f"It will take {periods // 12} years and {periods % 12} months to repay this credit!"


def calculate_annuity(principal, periods, interest):
    annuity = math.ceil(principal * ((interest * math.pow(1 + interest, periods)) /
                                     (math.pow(1 + interest, periods) - 1)))

    if (annuity * periods) > principal:  # adds overpayment to the output if applicable
        return f"Your annuity payment = {annuity}!\n" \
               f"Overpayment = {(annuity * periods) - principal}"
    else:  # runs if there is no overpayment
        return f"Your annuity payment = {annuity}!"


def calculate_principal(annuity, periods, interest):
    principal = math.floor(annuity / ((interest * math.pow(1 + interest, periods)) /
                                      (math.pow(1 + interest, periods) - 1)))

    if (annuity * periods) > principal:  # adds overpayment to the output if applicable
        return f"Your credit principal = {principal}!\n" \
               f"Overpayment = {(annuity * periods) - principal}"
    else:  # runs if there is no overpayment
        return f"Your credit principal = {principal}!"


def calculate_diff(principal, periods, interest):
    diff_list = []
    payment_sum = 0
    for current_period in range(1, periods + 1):  # appends payment for each month to diff_list
        diff = math.ceil((principal / periods) + interest * (principal - (principal * (current_period - 1) / periods)))
        diff_list.append(f"Month {current_period}: payment is {diff}")
    for diff in diff_list:  # adds all monthly payments together to determine overpayment
        payment_sum += int((re.findall("[0-9]*$", diff)[0]))
    if payment_sum > principal:  # adds overpayment to the output if applicable
        diff_list.append(" ")
        diff_list.append(f"Overpayment = {payment_sum - principal}")
        return diff_list
    else:  # runs if there is no overpayment
        return diff_list


# command line argument parsing


parser = argparse.ArgumentParser()
list_arguments = ["--type", "--annuity", "--principal", "--periods", "--interest"]

for argument in list_arguments:
    parser.add_argument(argument)

args = parser.parse_args()


# entry point calls


# this if statement checks that at least four arguments were entered, that interest
# was not left empty, and that none of the numerical parameters contain a negative number
if len(sys.argv) >= 4 and args.interest is not None and \
        not bool(re.match(".*-", f"{args.annuity}, {args.principal}, {args.periods}, {args.interest}")):
    if args.type == "annuity":
        print(type_annuity(args.annuity, args.principal, args.periods, args.interest))
        exit()
    if args.type == "diff" and args.annuity is None:
        # this print statement incrementally prints each element of diff_list on a new line
        print(*type_diff(args.annuity, args.principal, args.periods, args.interest), sep="\n")
        exit()
    else:
        print("Incorrect parameters")
        exit()
else:
    print("Incorrect parameters")
    exit()


# END OF PROGRAM
