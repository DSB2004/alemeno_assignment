
from .models import Loans
from django.utils import timezone

def calculate_credit_score(customer):
    loans = Loans.objects.filter(customer=customer)

    # incase user haven't taken any loans
    if not loans.exists():
        return 50  

    total_amount_taken = 0
    current_debt =0 
    current_emi=0
    for loan in loans:
        total_amount_taken=loan.loan_amount
        current_debt+= max(loan.tenure - loan.emi_paid_on_time, 0) * loan.monthly_payment
        if(loan.tenure - loan.emi_paid_on_time>0):
            current_emi+=loan.monthly_payment


    # If sum of current loans of customer > approved limit of customer , credit score = 0
    # If sum of all current EMIs > 50% of monthly salary , don’t approve any loans

    if current_debt > customer.approved_limit or current_emi>0.5*customer.monthly_salary:
        return 0


    # Past Loans paid on time
    total=loans.count()
    on_time_paid=0
    to_be_paid=0
    for loan in loans:
        on_time_paid+=loan.emi_paid_on_time
        to_be_paid+=loan.tenure

    # or 40 percent of the score depends upon the on time paid emi
    on_time_score=(on_time_paid/to_be_paid)*40 
        
        
    # Loan activity in current year 
    current_year = timezone.now().year
    current_year_loans = loans.filter(date_of_approval__year=current_year).count()

        

    score = 0
    # 40 % solely depends upon how much on time the person is paying the EMI
    score += on_time_score     
    # more the no of loans less score to get a loan
    score += max(0, 20 - total)      
    # assuming any person can have about 5 loans per year so  
    score += max(0,(1 - current_year_loans/5)*20) 
    # 20 percent goes for loan approved volume
    score += max(0, 20 - (total_amount_taken / customer.approved_limit) * 20)

    return round(min(100, score))



def get_interest_rate(credit_score):
    if(credit_score>50):
        return 0
    elif(credit_score<=50 and credit_score>=30):
        return 12
    elif(credit_score<30 and credit_score >=10):
        return 16
    else:
        return -1
    
    

def calculate_emi(principal, interest_rate, tenure):
    r = (interest_rate / 100) / 12  
    n = tenure

    if r == 0:
        return principal / n

    emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return round(emi, 2)