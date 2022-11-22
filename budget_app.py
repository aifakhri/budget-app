class Category:
  
	def __init__(self, category):
		self.category = category
		self.ledger = []
		self.total = 0.0

	def __str__(self):
		category_length = len(self.category)
		marker = int((30-category_length)/2)

		if (30-category_length)%2 == 1:
			header = f"{(marker+1)*'*'}{self.category}{marker*'*'}"
		elif(30-category_length)%2 == 0:
			header = f"{marker*'*'}{self.category}{marker*'*'}"

		texts = []
		for content in self.ledger:
			diff_len = 23 - len(content['description'])

			if diff_len <= 0:
				content['description'] = content['description'][:23]
			elif diff_len > 0:
				content['description'] = content['description'].ljust(23)

				content['amount'] = "{0:.2f}".format(content['amount'])

				text = content['description']+content['amount'].rjust(7)
				texts.append(text)      
		contents = '\n'.join(texts)

		total_amt = 'Total: ' + '{0:.2f}'.format(self.total)

		receipt = "\n".join([header, contents, total_amt])

		return receipt
	  
  
	def deposit(self, amount, description=''):
		self.total = self.total + amount
		self.ledger.append(
			{
			'amount': float(amount),
			'description': description
			}
		)

	def withdraw(self, amount, description=""):
		if amount > self.total:
			return False
		else:
			self.total = self.total - amount
			self.ledger.append(
			{
				'amount': float(-amount),
				'description': description,
			}
			)
			return True

	def get_balance(self):
		return self.total

	def transfer(self, amount, category):
		if amount > self.total:
			return False
		else:
			self.total = self.total - amount
			self.ledger.append(
			{
				'amount': float(-amount),
				'description': f"Transfer to {category.category}"
			}
			)
			category.deposit(amount, f"Transfer from {self.category}")
			return True
		
	def check_funds(self, amount):
		if amount > self.total:
			return False
		else:
			return True


def create_spend_chart(categories):
	category_names = list()
	category_spending = list()
	
	for category in categories:
		category_names.append(list(category.category))
	
	for spending in category.ledger:
		if float(spending['amount']) < 0.0:
			category_spending.append(float(spending['amount']))

	contents = [[f"{str(i).rjust(3)}| " for i in reversed(range(0,110,10))]]
	total_spending = sum(category_spending)
	
	for spending in category_spending:
		percentage = (spending/total_spending)*100
		content= [f"{'   ' if percentage < i else 'o  '}" for i in reversed(range(0,110,10))]
		contents.append(content)    

	for i, content in enumerate(contents):
		if i == 0:
			y_axes = contents[0]
			continue
		for j, data in enumerate(content):
			y_axes[j] = y_axes[j] + data

	max_name_len = max(category_names, key=len)
	for i, name in enumerate(category_names):
		diff_len = len(max_name_len) - len(name)
		name.extend(diff_len*" ")
		if i == 0:
			x_axes = category_names[0]
			continue
	
	for j, data in enumerate(name):
		x_axes[j] = x_axes[j] + "  " + data
	
	# print(x_axes)
	x_axes = '  \n'.join([x.rjust(len(x)+5) for x in x_axes])
	y_axes = '\n'.join(y_axes)
	graph = 'Percentage spent by category\n' + y_axes + "\n    ----------\n" + x_axes + '  '
	
	return graph