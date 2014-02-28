#!/usr/bin/python
#Author : Satishkumar masilamani, University of texas @Arlington
#Date : 25-Feb-2014
#Description : This program was written for Zappos Software Engineering Colleger Intern Position
#				In order to facilitate better gift-giving on the Zappos website, the Software Engineering team 
#				would like to test a simple application that allows a user to submit two inputs: N (desired # of products) 
#				and X (desired dollar amount). The application should take both inputs and leverage the 
#				Zappos API (http://developer.zappos.com/docs/api-documentation) to create a list of Zappos products 
#				whose combined values match as closely as possible to X dollars.

from urllib import urlopen
from json import loads as jsonloads

DesiredDollarAmount = 0  									#Stores the total amount planned to spend
DesiredNoOfProducts = 0  									#Stores the total number of products planned to buy
PriceOfEachProduct = [0]  									#Stores the price of each product to use while searching
SplitAmountEqually = ""  									#Indicates whether the price has to be equally distributed
Remainder = 0  												#If the money is equally distributen then we need to add the remainder to one of the product
Amount = 0  												#Stores the amount of each product to be assigned too
LoopRun = True  											#indicates when the loop has to be terminated
PartialAmount = 0  											#strores the amount the user inputs for each product
PartialTotalAmount = 0  									#stores the sum of the amount the user inputs
Count =0  													#Counter to check the number of times the loop was run
MinimumMoneyForOtherProducts = 0  							#Assumed to spare atleast 10$ for the remaing products each
#ReturnedItems = []  										#Stores the list of items 
SelectedItemsAttribute = []  								#Stores the product ID of each product that has been selected
FinalItemsSelected = []  									#Stores all the details of the products that has been selected
TotalEstimatedCost = 0.00  									#Stores the total cost of the products that is selected through this app
ApiKey = "&key=52ddafbe3ee659bad97fcce7c53592916a6bfd73"  	#Stores the Api Key used to retrieve the data from zappos

#def SelectAnItem(SearchingProductPrice,SelectedItemsAttribute):
#This function returns of the items which fits for the price range provided
#the result is already sorted based on the product popularity
#We limit the result to 10 products, by default it returns only 10 products but
#still the value has been provided to make sure the same
def SelectAnItem(SearchingProductPrice):
	#since most of the products in zappos ends with .99 cents we are searching for that particular value
	SearchingProductPrice = int(SearchingProductPrice) - 0.01
	#if the price range is greater than zero then only run the loop else dont.
	while(SearchingProductPrice > 0 ):
		#Stores the base url which will used to retrieve the information
		BaseReq = "http://api.zappos.com/Search/term/%20?"
		#We would like the limit the result to 10
		ItemLimit = "&limit=" + `10`
		#filtering based on the price
		Facets = "&filters={\"price\":[\"" + str(SearchingProductPrice) + "\"]}"
		#sorting the product based on its popularity
		Sorting = "&sort={\"productPopularity\":\"desc\"}"
		#concatenating the URL
		RequestURL = BaseReq + ItemLimit + Facets + Sorting + ApiKey
		#call to the API to get the reqult
		JsonResult = jsonloads(urlopen(RequestURL).read())
		#Check if the result has some values
		if(JsonResult.has_key('results')):
			#we need to put one product to our list, once its done return/exit the function
			#the product we select might be in the 1st/2nd/3rd place and so on so we have used the for loop
			for JsonResultDetails in JsonResult['results']:
				#check if the product has been selected already
				if JsonResultDetails['productId'] not in SelectedItemsAttribute:
					#if not selected already then select it and return
					SelectedItemsAttribute.append(JsonResultDetails['productId'])
					FinalItemsSelected.append(JsonResultDetails)
					return FinalItemsSelected
		else:
			#if there are no products returned then break and exit the function
			print "No product could be selected for the price : " + `SearchingProductPrice`
			SearchingProductPrice -= 1
			if Count != DesiredNoOfProducts:
				PriceOfEachProduct[Count+1] += 1

print "	We will suggest you with the products in your range. "
print " Please Enter the Amount(Integer) that you would like to spend on shopping and the number of gifts you are looking to buy"
while True:
	#get the user desire input
	DesiredDollarAmount = input("\nPlease enter the amount you would like to spend : ")
	DesiredNoOfProducts = input("Please enter the number of items you want to purchase : ")
	#check if the inputs are valid, if yes then exit the while loop
	if (DesiredDollarAmount > 0 and DesiredNoOfProducts >0 and DesiredNoOfProducts < 10):
		break
	else: #if the values are not valid check for the appropriate error message
		#since the limit of retrieving data is for only 10 products, we have limited the number of products
		#not to be more than 10.
		if DesiredNoOfProducts >10:
			print "\nThe number of products cannot be more than 10, please enter a value lesser than 10"
		else:
			print "\nPlease enter the Amount and Products greater than zero"
#if the user wish to split the amount equally with all the products or not
SplitAmountEqually = raw_input("Do you want to split the Amount equally into all the gifts (Y/N) : ")

#if user wants to distribute equally
if (SplitAmountEqually == "Y"):
	#run the for loop based on the number of products to be selected.
	for x in xrange(DesiredNoOfProducts):
		#for the first product add the remainder of the modulo
		if (x == 0):
			Remainder = (DesiredDollarAmount % DesiredNoOfProducts)
			Amount = ((DesiredDollarAmount - Remainder) / DesiredNoOfProducts) + Remainder
		#for other products just assign the value.
		else: 
			Amount = ((DesiredDollarAmount - Remainder) / DesiredNoOfProducts)
		PriceOfEachProduct.append(Amount)
#if the user wish to assign different values for different products then ask the user.
else:
	#run the for loop based on the number of products
	for x in xrange(DesiredNoOfProducts):
		#variable used to check if the value entered by the user is valid
		LoopRun = True
		#calculate the minimum amount required for other products and minus this with the total value
		MinimumMoneyForOtherProducts =  ((DesiredNoOfProducts-x-1) * 10)
		while LoopRun:
			PartialAmount = input("\nPlease enter the Amount to be spent on product " + `(x+1)` + ' : ')
			PartialTotalAmount = sum(PriceOfEachProduct)
			#if the amount entered by the user is more than the amount that could be allocated then throw a message and asg again for the user input
			if (((PartialAmount + PartialTotalAmount) > (DesiredDollarAmount - MinimumMoneyForOtherProducts)) or (PartialAmount <=0)):
				print "Please enter the amount greater than zero and lesser than or equal to " + `(DesiredDollarAmount - sum(PriceOfEachProduct) - MinimumMoneyForOtherProducts)`
			else:
				LoopRun = False
		PriceOfEachProduct.append(PartialAmount)
while True:
	Count+=1
	#call to select the item based on the current product price
	SelectAnItem(PriceOfEachProduct[Count])
	#if the number of products to be selected equals the count then break the loop
	if (Count == DesiredNoOfProducts) :
		break
#print FinalItemsSelected
Count = 1
#print the details of the products that was selected. 
for item in FinalItemsSelected:
	print `Count` + ". Product Name : " + item['brandName'] + "(ID : " + item['productId'] + ")"
	print "   Product URL : " + item['productUrl']
	print "   Brand Name : " + item['brandName']
	print "   Price : " + item['price'] + "   Original Price : " + item['originalPrice']
	print "   Discount : " + item['percentOff']
	#strip only the price for the item[price] value, this will be in the format $99.99
	price = item['price'][1:]
	#calculate the total estimate
	TotalEstimatedCost += float(price)
	Count+=1
print "Total Estimated cost is : $" +`TotalEstimatedCost`
print "Budget : $" + `DesiredDollarAmount` + " Total Number of products : " + `DesiredNoOfProducts`