from collections import defaultdict
#Oke so for this we need several classes.
#We need a class to hold the customer, region and product data. These classes will hold our KPI data.
#Now this setup would be a bit mutch for this small use case but it is nice to show classes.
#In our main file we can inport the tree child classes for use

class KPI():
    def __init__(self) -> None:
        self.quantity:int = 0
        self.total:int = 0
    
    #Normaly we can create methods here for the KPI class, but for this simple use case no class methods are needed.

class product(KPI):
    def __init__(self) -> None:
        super().__init__()
        self.region_sale:defaultdict = defaultdict(int) 
        self.customer_sale:defaultdict = defaultdict(int)

class customer(KPI):
    def __init__(self) -> None:
        super().__init__()
        self.region_sale:defaultdict = defaultdict(int)
        self.product_sale:defaultdict = defaultdict(int)

class region(KPI):
    def __init__(self) -> None:
        super().__init__()
        self.product_sale:defaultdict = defaultdict(int)
        self.customer_sale:defaultdict = defaultdict(int)
