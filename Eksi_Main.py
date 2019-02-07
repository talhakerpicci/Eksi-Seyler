import requests
from bs4 import BeautifulSoup
import time

import News_Database
import User_Database
import Inform_User


News = News_Database.Database_Post()
Mail = User_Database.Database_User()

print("""
Enter '1' to organize user database.
Enter '2' to start the program.
Enter 'q' to exit program.
""")

while True:

	number = input("Command: ")

	if (number == "1"):

		print("""
		Enter '1' to see all users.
		Enter '2' to add a new user.
		Enter '3' to delete a user.
		Enter '4' to update a user.
		Enter '5' to see total number of users.
		Enter '6' to go back to main menu.
		Enter 'q' to exit the program.
		""")

		while True:

			command = input("\nCommand for mail: ")

			if (command == "1"):
				Mail.show_mails()

			elif (command == "2"):
				print("Enter a new mail address:")
				new_mail = input().lower()

				if (Mail.check_if_mail_exists(new_mail)):
					print("\n" + new_mail, "already exists on database. Please try again.\n")
					continue

				print("Would you want to receive mails? (Y/N):")
				user_stat = input().upper()

				if (user_stat == "Y"):
					user_stat = True
					text = new_mail + " successfully added to database."

				elif (user_stat == "N"):
					user_stat = False
					text = new_mail + " successfully added to database. Be aware that you wont receive any mails."

				else:
					print("\nInvalid command. Try again.\n")
					continue

				new_user = User_Database.User(new_mail, user_stat)
				Mail.add_mail(new_user)

				print(text)


			elif (command == "3"):

				if (Mail.total_user() == 0):
					print("\nNo user found on database.\n")
					continue

				print("Enter the mail address you want to delete:")
				del_mail = input("Mail: ")

				if (Mail.check_if_mail_exists(del_mail) == 0):
					print("There is not such mail address as " + del_mail + ". Please try again")
					continue

				print("Are you sure you want to delete " + del_mail + "? (Y/N):")
				yes_no = input().upper()

				if (yes_no == "Y"):
					Mail.delete_mail(del_mail)
					print(del_mail, " successfully deleted from database.")

				elif (yes_no == "N"):
					print("Process canceled.")
					continue
				else:
					print("\nInvalid command. Please try again.")


			elif (command == "4"):

				if (Mail.total_user() == 0):
					print("\nNo user found on database.\n")
					continue

				print("Enter the mail address you want to update: ")
				update_mail = input()

				if (Mail.check_if_mail_exists(update_mail) == 0):
					print("There is not such mail address as " + update_mail + ". Please try again")
					continue

				print("What would you want to change? "
					  "To go back, enter 'q' , to change mail, "
					  "enter M, to change status, enter S:")

				change_what = input().upper()

				# Updating User Mail
				if (change_what == "M"):
					new_mail = input("Enter a new mail address: ")
					Mail.update_mail(update_mail, new_mail)
					print(update_mail, "changed to", new_mail + ".")

				# Updating Status (if 0, wont receive mails, else will)
				elif (change_what == "S"):
					print("Would you want to get mails or not? (Y/N)")
					yes_no = input().upper()
					if (yes_no == "Y"):
						Mail.update_stat(update_mail, True)
						print(update_mail, "will now receive mails.")
					elif (yes_no == "N"):
						Mail.update_stat(update_mail, False)
						print(update_mail, "will not receive mails anymore.")
					else:
						print("Wrong command. Please try again.")
						continue

				elif (change_what == "Q"):
					print("You are back to menu.")

				else:
					print("\nInvalid comamnd. Try again.\n")


			elif (command == "5"):

				total = Mail.total_user()

				if (total != 0):
					print("Total number of users: ", total)
				else:
					print("No user found on database.")

			elif (command == "6"):
				# Going Back to Main Menu
				print("\nYou are on main menu right now.\n")
				break

			elif (command == "q"):
				exit()

			else:
				print("Invalid command. Try again.")


	elif (number == "2"):

		while True:

			new_posts = 0

			# Checking if there are any users on database
			if (Mail.total_user() == 0):

				print("No user found on database. You have to add at least one user to continue.")
				user_mail = input("Mail: ").lower()
				print("Would you want to receive mails?")
				print("(If you are running this program for the first time, \nwe recommend "
					  "turning notifications off if you don't\nwant get several mails"
					  " in your first run.\nAfter the first run, the posts will be added to database"
					  " and you can turn notifications on.)")

				stat = input("Y/N: ").upper()

				# Checking Stat
				if (stat == "Y"):
					stat = True
				elif (stat == "N"):
					stat = False
				else:
					print("\nWrong command. Try again.\n")
					continue

				user_info = User_Database.User(user_mail, stat)

				# Adding user to database
				Mail.add_mail(user_info)

				print(user_mail, "successfully added to database.")


			html_content = ""
			try:
				url = "https://seyler.eksisozluk.com/"
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
				response = requests.get(url, headers=headers)
				html_content = response.content

			except:
				print("Something unexpected happened.")
				time.sleep(300)

			soup = BeautifulSoup(html_content, "html.parser")
			item_html = soup.find_all("div", {"class": "col-flex"})

			html_content = """"""

			for i in item_html:
				html_content += str(i) + "\n"

			soup = BeautifulSoup(html_content, "html.parser")

			link_html = soup.find_all("a")
			text_html = soup.find_all("span", {"class": "hero-headline"})
			images_html = soup.find_all("img", {"class": "hero-img"})

			links = []
			headlines = []
			images = []

			for i in link_html:
				links.append(i['href'])

			for i in text_html:
				headlines.append(
					str(i.text).replace("\n", "").replace("                  ", "").replace("                ", ""))

			for i in images_html:
				i = str(i['style']).replace("background-image: url('", "").replace("')", "")
				images.append(i)

			# for i,j,k in zip(links,headlines,images):
			# print(i,"\n",j,"\n",k)
			# print("------------------------------")

			for link, headline, image in zip(links, headlines, images):
				url = link
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
				response = requests.get(url, headers=headers)
				html_content = response.content
				soup = BeautifulSoup(html_content, "html.parser")

				date_html = soup.find("span", {"class": "meta-date"})
				date = str(date_html.get_text())
				date = date.replace("        ", "").replace("\n", "").replace("\r", "")
				date_sql = date

				if (date[0].isdigit() and date[1].isdigit()):
					date = int(str(date[0] + date[1]))
				elif (date[0].isdigit()):
					date = int(date[0])

				day = int(time.strftime("%d"))

				if (date == day and not News.check_if_post_exists(link)):
					read_num_html = soup.find("b")
					read_num = read_num_html.get_text()

					genre_html = soup.find("div", {"class": "col-xs-5 meta-category"})

					genre_link = "https://seyler.eksisozluk.com" + str(genre_html.a.get('href'))
					genre = genre_html.a.get_text().replace("\n", "").replace("        ", "")

					size = "big"

					Post = News_Database.News(headline,genre,genre_link,date_sql,read_num,link,image,size)
					News.add_post(Post)

					mail_list = Mail.get_mails()

					text_mail = Post.text_of_mail()

					new_posts += 1

					for user in mail_list:
						Inform_User.send_mail(user[0],text_mail)

			try:
				url = "https://seyler.eksisozluk.com/"
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
				response = requests.get(url, headers=headers)
				html_content = response.content

			except:
				print("Something unexpected happened.")
				time.sleep(300)

			soup = BeautifulSoup(html_content, "html.parser")
			item_html = soup.find_all("div", {"class": "col-md-8"})

			html_content = """"""

			for i in item_html:
				html_content += str(i) + "\n"

			soup = BeautifulSoup(html_content, "html.parser")

			small_items_html = soup.find_all("div",{"class":"col-sm-4"})
			medium_item_html = soup.find("div",{"class":"col-sm-8"})

			small_item_read_num_html = soup.find_all("span",{"class":"meta-stats"})
			small_item_headline_html = soup.find_all("div",{"class":"content-title"})

			small_links = []
			small_headlines = []
			small_genres = []
			small_genre_links = []
			small_read_num = []
			small_images = []

			medium_link = ""
			medium_headline = ""
			medium_genre = ""
			medium_genre_link = ""
			medium_read_num = ""
			medium_image = ""

			for i,j in zip(small_items_html,range(4)):
				small_links.append(i.a['href'])
				small_genre_links.append("https://seyler.eksisozluk.com" + str(i.span.a['href']))
				small_genres.append(str(i.span.text).replace("\n", "").replace("        ", "").replace("  ",""))
				small_images.append(i.img['data-src'])

			for i,j in zip(small_item_read_num_html,range(5)):
				text = (str(i.text).replace("      ","").replace("\r","").replace("\n","").replace("    ",""))
				small_read_num.append(text)

			medium_read_num = small_read_num[1]

			small_read_num.__delitem__(1)

			for i,j in zip(small_item_headline_html,range(5)):
				small_headlines.append(str(i.text).replace("\r","").replace("\n","").replace("      ","").replace("    ",""))

			medium_headline = small_headlines[1]

			small_headlines.__delitem__(1)


			for link, headline, genre, genre_link, read_num, image in zip(small_links, small_headlines, small_genres, small_genre_links, small_read_num, small_images):

				url = link
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
				response = requests.get(url, headers=headers)
				html_content = response.content
				soup = BeautifulSoup(html_content, "html.parser")

				date_html = soup.find("span", {"class": "meta-date"})
				date = str(date_html.get_text())
				date = date.replace("        ", "").replace("\n", "").replace("\r", "")
				date_sql = date

				if (date[0].isdigit() and date[1].isdigit()):
					date = int(str(date[0] + date[1]))
				elif (date[0].isdigit()):
					date = int(date[0])

				day = int(time.strftime("%d"))

				if (date == day and not News.check_if_post_exists(link)):

					size = "small"

					Post = News_Database.News(headline, genre, genre_link, date_sql, read_num, link, image, size)
					News.add_post(Post)

					mail_list = Mail.get_mails()

					text_mail = Post.text_of_mail()

					new_posts += 1

					for user in mail_list:
						Inform_User.send_mail(user[0], text_mail)



			medium_link = medium_item_html.a['href']
			medium_genre = str(medium_item_html.span.text).replace("\n", "").replace("        ", "").replace("  ","")
			medium_genre_link = "https://seyler.eksisozluk.com" + str(medium_item_html.span.a['href'])
			medium_image = medium_item_html.img['data-src']

			url = medium_link
			headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			response = requests.get(url, headers=headers)
			html_content = response.content
			soup = BeautifulSoup(html_content, "html.parser")

			date_html = soup.find("span", {"class": "meta-date"})
			date = str(date_html.get_text())
			date = date.replace("        ", "").replace("\n", "").replace("\r", "")
			date_sql = date

			if (date[0].isdigit() and date[1].isdigit()):
				date = int(str(date[0] + date[1]))
			elif (date[0].isdigit()):
				date = int(date[0])

			day = int(time.strftime("%d"))

			if (date == day and not News.check_if_post_exists(medium_link)):

				size = "medium"

				Post = News_Database.News(medium_headline, medium_genre, medium_genre_link, date_sql, medium_read_num, medium_link, medium_image, size)
				News.add_post(Post)

				mail_list = Mail.get_mails()

				text_mail = Post.text_of_mail()

				new_posts += 1

				for user in mail_list:
					Inform_User.send_mail(user[0], text_mail)


			print("Process finished. " + str(new_posts) + " new post released. Waiting for 3 min.")
			time.sleep(180)


	elif (number.lower() == "q"):
		exit()

	else:
		print("Invalid command. Try again.")