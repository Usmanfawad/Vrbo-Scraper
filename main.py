from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import *
import datetime
import re
import time



class VrboScraper:

    def __init__(self):
        self.url = ""
        self.file_name = ""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.room_links = []
        self.GUI()

    def GUI(self):
        COLOUR_ONE = "#222831"
        COLOUR_TWO = "#393E46"
        COLOUR_THREE = "#FFD369"
        COLOUR_FOUR = "#EEEEEE"

        self.root = Tk()
        self.root.geometry("600x700")
        self.root.configure(bg=COLOUR_ONE)
        Label(text="VRBO SCRAPER", font="Helvetica 14 bold",fg=COLOUR_THREE,bg=COLOUR_ONE).pack(padx=50,pady=50,side=TOP,expand=0,fill=BOTH)

        frame_one = Frame(self.root,bg=COLOUR_ONE)
        frame_one.pack(side=TOP,ipadx=50,ipady=10,fill="x")
        Label(frame_one,text="Browser URL", font="Helvetica 11 italic",fg=COLOUR_THREE,bg=COLOUR_ONE).pack(side=LEFT,padx=(70,10),expand=0,fill=BOTH)
        url_entry = StringVar()
        entry_box_url = Entry(frame_one,fg=COLOUR_ONE,bg=COLOUR_THREE,justify = CENTER,textvariable=url_entry)
        entry_box_url.pack(side=RIGHT,padx=50,ipadx = 100, ipady = 5)
        entry_box_url.focus_force()

        frame_middle = Frame(self.root,bg=COLOUR_ONE)
        frame_middle.pack(side=TOP,ipadx=50,ipady=10,fill="x")
        Label(frame_middle,text="File Name      ", font="Helvetica 11 italic",fg=COLOUR_THREE,bg=COLOUR_ONE).pack(side=LEFT,padx=(70,10),expand=0,fill=BOTH)
        file_entry = StringVar()
        entry_box_file = Entry(frame_middle,fg=COLOUR_ONE,bg=COLOUR_THREE,justify = CENTER,textvariable=file_entry)
        entry_box_file.pack(side=BOTTOM,padx=50,ipadx = 100, ipady = 5)

        def save_url():
            self.url = url_entry.get()
            self.text.insert(END,"\n\nEntered URL: "+ self.url)
            self.text.see("end")
            self.file_name = file_entry.get() + ".csv"
            with open(self.file_name,"w") as f:
                f.writelines("Room Link,Full location,Hosted by,Host title,Propery Number,Member since\n")
            f.close()
            self.Scrape()

        frame_two = Frame(self.root,bg=COLOUR_ONE)
        frame_two.pack(side=TOP,ipadx=50,ipady=10,fill="x")

        self.text = Text(frame_two, font="Helvetica 9 italic",bg=COLOUR_ONE,fg=COLOUR_THREE)
        run_script = Button(frame_two,text="Run Script",font="Helvetica 11 italic",fg=COLOUR_ONE,bg=COLOUR_THREE, command=save_url)
        run_script.pack(side=BOTTOM,pady=20,ipady=2,ipadx=10)
        self.text.pack(side=TOP,ipady=50, ipadx=90,padx=50,pady=(20,0))
        self.text.insert(END,"\n"+"\nEnter URL in the box above.\nOnce Entered, click the button below.\nScrapped data status will be shown here")
        self.text.see("end")
        self.Refresh_Gui()
        self.root.mainloop()


    def Refresh_Gui(self):
        self.root.update_idletasks()
        self.root.update()

    def scroll_down(self):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(0.8)
            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def Scrape(self):
        now = datetime.datetime.now()
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        start_time = "Start time | {}:{}".format(hour,minute)
        self.text.insert(END,"\n\n"+"---"+str(start_time)+"---")
        self.text.see("end")
        self.Refresh_Gui()
        self.root.update_idletasks()
        self.root.update()

        # ------------------------------ FOR MAC OS ------------------------------
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # self.text.insert(END,"\n"+"\n\n\n> ATTEMPTING TO INSTALL CHROMEDRIVER")
        # self.text.see("end")
        # self.Refresh_Gui()
        # driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)


        # ------------------------------ FOR WINDOWS------------------------------
        print("\n\n\n----------- ATTEMTING TO INSTALL CHROMDRIVER -----------")
        self.text.insert(END,"\n"+"\n\n\n> ATTEMPTING TO INSTALL CHROMEDRIVER")
        self.text.see("end")
        self.Refresh_Gui()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        
        
        print("\n"*100)
        # print("\n\n\n--------- CHROMDRIVER INSTALLATION SUCCESSFULL -----------")
        self.text.insert(END,"\n"+"> CHROMEDRIVER INSTALLATION SUCCESSFULL\n")
        self.text.see("end")
        self.Refresh_Gui()
        # print("\n\n\n------------- YOUR DATA IS BEING EXTRACTED ---------------")
        self.text.insert(END,"\n"+"\n\n> YOUR DATA IS BEING EXTRACTED\n\n")
        self.text.see("end")
        self.Refresh_Gui()


        BASE_URL = 'https://www.vrbo.com/'

        #Finding the number of pages and then a variable that stores the number of pages
        #Each page contains 50 rooms.
        self.driver.get(self.url)
        time.sleep(2)
        #scroll to the bottom of the page to find the page element
        # self.scroll_down()
        # time.sleep(2)
        # page_container = self.driver.find_element(By.CLASS_NAME,"Pager__li")
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        for scroll in range(5):
            self.driver.execute_script("scrollBy(0,-100);")
            time.sleep(0.3)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Pager"))
            )
        page_container_li = self.driver.find_element(By.CLASS_NAME,"Pager__li--page")
        li_span = page_container_li.find_element(By.TAG_NAME,"span")
        splitted_li_span = li_span.text.split(" ")
        if "+" in splitted_li_span[-1]:
            removed_plus_sign = int(splitted_li_span[-1].replace("+",""))
            # print(type(removed_plus_sign))
        else:
            removed_plus_sign = int(splitted_li_span[-1])
        
        # string = "https://www.vrbo.com/en-gb/search/keywords:orlando-florida-united-states-of-america/arrival:2022-01-17/departure:2022-01-22/minNightlyPrice/0?adultsCount=2&petIncluded=false&filterByTotalPrice=true&ssr=true"
        string = self.url
        occur = 6  # on which occourence you want to split

        indices = [x.start() for x in re.finditer("/", string)]
        part1 = string[0:indices[occur-1]]
        part3 = string[indices[occur-1]+1:]
        print(part1)
        print(part3)
        
        page_count = 1
        for x in range(0, removed_plus_sign, 50):
        # for x in range(0, 101, 50):
            part2 = f"/page:{page_count}/"
            page_count += 1
            print(part2)
            self.driver.get(part1+part2+part3)
            self.scroll_down()
            time.sleep(2)
            recentList = self.driver.find_elements(By.CSS_SELECTOR,"div[data-wdio*=Waypoint]") 
            
            for list in recentList :
                self.driver.execute_script("arguments[0].scrollIntoView();", list )
                time.sleep(0.3)
                links_tag = list.find_element(By.TAG_NAME,"a")
                href_attr = links_tag.get_attribute('href')
                self.room_links.append([href_attr])

            
                
        for each_page in range(len(self.room_links)):
            self.driver.get(self.room_links[each_page][0])
            self.scroll_down()

            #Waiting for hostname to appear
            WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*=owner-details__name]"))
                        )

            #finding the address
            full_address = self.driver.find_element(By.CSS_SELECTOR,"ul[class*=HeadlineBreadcrumbs]") 
            each_address = full_address.find_elements(By.TAG_NAME,"li > a")
            for per_address in each_address:
                address = per_address.text
            self.room_links[each_page].append(address)

            #Owner/Hosted by
            hosted_by_element = self.driver.find_element(By.CSS_SELECTOR,"div[class*=owner-details__name]")
            hosted_by_p_element = hosted_by_element.find_element(By.TAG_NAME,"h2").text
            self.room_links[each_page].append(hosted_by_p_element)

            #host title
            try:
                host_title = self.driver.find_element(By.CSS_SELECTOR,"p[class*=host-summary__title]")
                host_title_text = host_title.text
                self.room_links[each_page].append(host_title_text)
            except:
                print("No title")
                host_title_text = "-"
                self.room_links[each_page].append("-")
                
            #Finding the property number
            p_address = self.driver.find_element(By.CSS_SELECTOR,"p[class*=booking-assist__prop-unit]")
            self.room_links[each_page].append(p_address.text)

            #Member since
            membersince_element = self.driver.find_element(By.CSS_SELECTOR,"div[class*=owner-details__member-since]")
            member_since_text = membersince_element.text
            self.room_links[each_page].append(member_since_text)
            
            with open(self.file_name, "a") as f:
                f.writelines(self.room_links[each_page][0] + "," + address + "," + hosted_by_p_element + "," + host_title_text + ","  + p_address.text + "," + member_since_text +"\n")


        self.driver.close()
        

if __name__ == "__main__":
    VrboScraper()