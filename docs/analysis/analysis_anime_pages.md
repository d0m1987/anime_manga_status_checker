# Analysis of my favorite anime pages html structure

## Goal
This should document my thoughts and development of the scraper module for people that would like to learn scraping.

## Steps
1. [Analyse the pages you would like to scrape](#analyse-the-pages-you-would-like-to-scrape)
2. [Build a proof of concept](#build-a-proof-of-concept)

### Analyse the pages you would like to scrape
The basic idea was to scrape the following pages for updates:
- http://naruto-tube.org/
- https://dragonball-tube.com/
- http://fairytail-tube.org/
- https://onepiece-tube.com/

As a first start, you should get familiar with xpath. Xpath is a bit like regular expressions, just for xml structures.  
The following sources helped me a lot and are still used frequently:
- [W3Schools: always a great short overview](https://www.w3schools.com/xml/xpath_intro.asp)
- [Blog post on "The scrapinghub blog": great more in depth tutorial. Here I learned about the different node types Element, Attribute, Comment and Text. This helps later to understand commands like text() or comment() as node selectors in xpath.](https://blog.scrapinghub.com/2016/10/27/an-introduction-to-xpath-with-examples)

Now it's time to start digging in the pages. The goal is to find a most common node structure to identify the information we need. Using the "Inspect" function of Chrome, I got into the analysis of the html structure. By inspecting [this page](http://dragonball-tube.com/dragonball-super-mangaliste) I thought that the class "sagatable" could yield great results. It's close to the data I'd like to scrape (the info about the available chapters) and looks like this class is only used for the media content.  

![alt text][analysis_1]

Sadly, this didn't work out as planned. The other pages don't contain the class "sagatable". It looks like this class is only used on a few pages. Let's search for another structure!  

Since I'm interested in identifying the latest episodes, I dug one level deeper into the chapter rows themselves.  
  
As you can see, the chapter rows themselves have a class "mediaitem". This looks again promising! 

![alt text][analysis_2]

I checked different manga and anime pages withing dragonball-tube.com and they all worked. Great!  
Then I switched to the manga page for One Piece and there are no mediaitems. It looks like there is no one-stop-solution BUT let's check systematically how far we can go with the classes "sagatable" and "mediaitem".

|  URL  |  Manga or anime  |  class "sagatable" exists  |  class "mediaitem" exists  |
|:------------------:|:------------------:|:------------------:|:------------------:|
|  http://dragonball-tube.com/dragonball-super-episoden-streams  |  Anime  |  No  |  Yes  |
|  http://dragonball-tube.com/dragonball-super-mangaliste  |  Manga  |  Yes  |  Yes  |
|  http://dragonball-tube.com/galactic-patrol-mangaliste  |  Manga  |  No  |  Yes  |
|  https://onepiece-tube.com/episoden-streams  |  Anime  |  Yes  |  Yes  |
|  https://onepiece-tube.com/kapitel-mangaliste  |  Manga  |  Yes  |  `No`  |
|  http://fairytail-tube.org/episoden-streams  |  Anime  |  Yes  |  Yes  |
|  http://fairytail-tube.org/100-years-quest-mangaliste  |  Manga  |  No  |  Yes  |
|  http://fairytail-tube.org/edens-zero-mangaliste  |  Manga  |  No  |  Yes  |
|  http://naruto-tube.org/boruto-episoden-streams  |  Anime  |  Yes  |  Yes  |
|  http://naruto-tube.org/boruto-kapitel-mangaliste  |  Manga  |  Yes  |  Yes  |

As we can see, the class "mediaitem" looks good for selection EXCEPT for the One Piece manga list.  
I'm currently having two ideas in mind.
1. Use different xpath selectors for every page
2. Execute custom Javascript before running xpath to add the class "mediaitem" to the table rows.

I'm going with 1., since it looks to me less error prone, easier to read and maintainable. With 1., the HTML source code you see in the browser is exactly the same one the code is working with. Furthermore, it's easier to include future sites to scrape with this strategy.  

Now it's time to specify the exact xpath using xpath functions. Let's start with class "sagatable".

#### class "sagatable"
Let's start off with selecting all nodes and filter it down to the class "sagatable".

```xml
//*[@class="sagatable"]
```
This yields all the saga tables on the page. With //tr we can get all the table rows of the saga tables.

```xml
//*[@class="sagatable"]//tr
```

Since we are only interested in the last table row (i.e. the newest item), we use the last() function to get the last element.


```xml
//*[@class="sagatable"]//tr[last()]
```

If you try this on a page with multiple saga tables, you will receive multiple hits. The reason for this behaviour is, that the xpath `//*[@class="sagatable"]` returns a list of nodes with the class being sagatable. **For each element in this list of nodes**, we identify all the row tags `<tr></tr>` and return the last one.  
What we are looking for is the last row in the last sagatable. We can accomplish this via two ways.
1. `(//*[@class="sagatable"]//tr)[last()]` -> here we are turning all table rows into one list and selecting the last element on this list.
2. `//*[@class="sagatable"][last()]//tr[last()]` -> here we are selecting the last of the saga tables. Within this saga table, we select all rows and from these, we select the last one.

Because I like the more explicit reading of 2., I'll stick with this.

#### class "mediaitem"

The selection of the class "mediaitem" is analogous to the class "sagatable".
First we select all the table rows in the HTML source with

```XML
//tr[@class="mediaitem"]
```

Then, we filter it for the last (i.e. most recent) item with 
```XML
//tr[@class="mediaitem"][last()]
```

Again, we need to use brackets to build one list as follows
Then, we filter it for the last (i.e. most recent) item with 
```XML
(//tr[@class="mediaitem"])[last()]
```

Otherwise, we get again the last element of each table that has items with class "mediaitem".  
In this case, I do not know why we need to group it again, since `//tr[@class="mediaitem"]`returns a list of all the rows and we want to select the last one. If anyone who knows the reason reads this, please contact me. Credits are promised ;-)

### Build a proof of concept
Now it's time to start building a proof of concept. The first step is easy. Our goal is to 
1. Start selenium
2. Get the data from the test table

The pages for Dragonball run without problems **but** One Piece has a data protection notice overlay. This one is a bit tricky, because we cannot directly select and click the "Accept and close" button. It is hidden within an iFrame. See the following screenshot

![alt text][analysis_3]

To solve this problem, we switch to the iFrame, push the button and switch back. This is done with the following code:

```python
iframe = driver.find_element_by_xpath('//*[contains(@id,"sp_message_iframe")]')
driver.switch_to.frame(iframe)
driver.find_element_by_xpath('//button[@title="Accept and close"]').click()
driver.switch_to.default_content()
```

Remarks to this code snippet:
1. I use `//*[contains(@id,"sp_message_iframe")]`because I cannot be sure if the id of the iFrame is static. `sp_message_iframe_376736` looks to me, like it could be cached and change any time. Since there is no other element on the page with the id containing `sp_message_iframe` I assume this to be a robust way to select the iFrame.
2. I use `//button[@title="Accept and close"]` because I find it easy to read and understand what I'm selecting.  

Since we are just preparing a proof of concept (POC), we implement the closing of the data protection notice overlay in an easy way. If the element scraped via the xpath has no text value (assumption here: data protection notification is blocking), we try to close it.

Now the code is running and reading data from the websites. I added a time delay of five seconds between page updates since I do not want to harm the websites by creating too many requests.

Our first POC shows, what the last table row does not on contain on all pages the most recent chapter / episode information.  
For the page https://onepiece-tube.com/episoden-streams the last table row on that site has the value `001 Das Abenteuer beginnt 52 22.07.1997 Episode 4`.  
This is a problem that we will tackle in the next commit.

We are now tackling down the problem, that some sources do not have the newest item as the last table row. There are multiple ways to solve this problem:

1. We could use different xpath expressions per page. We could update One Piece to use `//*[@class="sagatable"][1]//tr[2]` instead of `//*[@class="sagatable"][last()]//tr[last()]`.  
Note, that we use `[1]...[2]`. This translates to the first sagatable and it's second row, because the first row is the header.  
2. We could stop using xpath expressions to find the latest chapters / episodes. Instead we could return all table rows with the driver function `find_elements_by_xpath`. Afterwards, we could analyse all the returned rows using Python.
3. The following is just an idea without proof if this can work. Maybe I'll try this one day.  
Since the episode number is always in the first column, we could use xpath functions to identify the max value of the first `<td></td>`in each row and return this row.  

For the ease of useage, we go with the approach 1.)

Now it's time to grab all the data we are looking for. Namely, this is
- Number of the episode
- Name of the episode
- Direct link to the episode

By inspecting the HTML structure of all the test sites, we can see that the episode number and episode name are always the first two `<td></td>` elements in the `<tr></tr>` element.

![alt text][analysis_4]

So our first step is to grab the episode number and name off the element we identified via xpath. The code for that is as follows:

```Python
element_tds = element.find_elements_by_tag_name("td")
episode_number = element_tds[0].text
episode_name = element_tds[1].text
```

Grabbing the direct link to the episode is a bit harder. As you can see in the screenshot below, the link to the episode is built via the attribute "onclick". 

![alt text][analysis_5]

With the `get_attribute` function of Selenium we can get the value for onclick. Using the library "parse", we can extract the needed information in an easy readable way. We could do the same with a regular expression, but in my opinion this would make the code less readable and is not necessary at this point.

```Python
onclick = element.get_attribute("onclick")
href_onclick = parse("window.location.href = '{}'", onclick)[0]
```

The git repository for the library "parse" can be found [here](https://github.com/r1chardj0n3s/parse)

Giving this code another run over our pages shows, that (again...) the manga site for One Piece has another structure. While all other pages have their "onclick" attribute in the `<tr></tr>`, this site has it in the `<td></td>` that holds the episode name.

This problem is solved with the following small adaption to our code that gets the "onclick" attribute value.

```Python
onclick = element.get_attribute("onclick") or element.find_element_by_xpath("//td[@onclick]").get_attribute("onclick")
href_onclick = parse("window.location.href = '{}'", onclick)[0] 
```

The `or` operator in Python returns as soon as any value resolves to true. The function `get_attribute` returns `None` if the element doesn't have the searched attribute.  
So the code first tries the more frequent case first and then, if that yields no results, he tries to find a `<td></td>` element with the "onclick" attribute.  
I could have coded it in a more direct way, i.e. directly access the second `<td></td>`, but chose otherwise because so the code might be more flexible.  

The last step before we have gathered all information needed is to get the first part of the url. As you can see we need to get the value of `window.location.href`. This can easily be done executing custom javascript code in Selenium.

```Python
href_window = driver.execute_script("return window.location.href")
```

Important here is to note the "return" statement. A common mistake I make is to forget the return and wondering afterwards, why the code executes without errors but doesn't return a value. Be warned about this error ;-)

Feel free to first try it in the console. I did so too. This helps to identify bugs easier, since you don't have another layer (Selenium) between you and the HTML source.

![alt text][analysis_6]

If you now run the POC, you see exactly the output we wish for:

![alt text][analysis_7]

Great! So at this point, we can get all the data we need. Now it's time to wrap this knowledge in good code!

### Refactoring the proof of concept

My plan was to deploy the scraper in a first version to my Raspberry Pi and then to a Virtual Private Server (VPS). In both cases I'd like to use Docker for deployment.  
Here I noticed, that I will run into problems, since my Raspberry Pi runs on an ARM chipset and my VPS runs on an Intel Xeon processor.  

The possibilities I had here were:  
- Address the problem by using adapted docker images for Selenium. Neither of the images I've seen so far are from a trusted source, so I might even need to build it myself if I'd like to trust it 100%. 
- Rethink about my code. Do I really need Selenium? Can I maybe reduce the dependencies by going back to pure HTML? Does this maybe even have more benefits?

I chose the latter approach. Why did I do that? There are a lot of benefits:  

- Use requests instead of Selenium. This helps in reducing the overhead. There is no dependency based on a working chromedriver or similar anymore.  
Furthermore, we do not need to worry about cookie consents that we need to click like before. They are based on Javascript and this is not run when using the requests library to get only the HTML source.
- Make the program more robust. Since we are using only python libraries that are independent of the chip architecture, we are only dependent on the Python runtime environment. And this exists on Raspbian as well as on Ubuntu (my server OS).

The (very small) problem that we cannot use the xpath parser from Selenium anymore when dropping it can easily be solved by using lxml as libray for parsing / working with HTML.

The general idea in the new file [poc_requests_lxml.py](poc_requests_lxml.py) is exactly as before. We are now just using pure html instead of loading the whole homepage.

[analysis_1]: ./img/analysis_1.png "HTML source code for sagatable with Chrome Inspect"
[analysis_2]: ./img/analysis_2.png "HTML source code for mediaitem with Chrome Inspect"
[analysis_3]: ./img/analysis_3.png "HTML source code for iFrame with Chrome Inspect"
[analysis_4]: ./img/analysis_4.png "HTML source code for table row and table data with Chrome Inspect"
[analysis_5]: ./img/analysis_5.png "HTML source code for attribute 'onclick' from table data element with Chrome Inspect"
[analysis_6]: ./img/analysis_6.png "Browser console execution of window.location.href"
[analysis_7]: ./img/analysis_7.png "Console results of the scraping"