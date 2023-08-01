# TLDR Scraper

This application will let you view articles from the `ai`, `tech` and `webdev` topics from the <a href="https://www.tldr.tech" target="_blank">TLDR Newsletter</a> in an easy-to-read web browser format as opposed to a list of links in an e-mail. If you're interested in other TLDR topics you can simply adjust the list of URLs in the `generate_links_html()` function within [app.py](app.py).

No subscription to TLDR is needed to view these links.

When the application starts, it will look for an existing file with the links for today's date. If found, it will populate the webpage with those links. If not, it will scrape the links from TLDR for today to populate the webpage. Note that TLDR does not post on weekends, so this will simply use the most recent Friday's links if ran on a weekend.

![](assets/screenshot.png)

You can run this application either locally or via Docker:

### Run Locally
1. Download and extract the code in this repository.
2. Install Python dependencies by running the following command in the extracted repository:
    ```
    pip install -r requirements.txt
    ```
3. Run the `app.py` Python file
4. Navigate to [localhost:8989](localhost:8989)


### Run in Docker
1. With Docker installed, pull the image from DockerHub:

    ```
    docker pull braundo30/tldr-scraper:latest
    ```

    ```
    docker run -p 8989:8989 braundo30/tldr-scraper:latest
    ```

2. Navigate to [localhost:8989](localhost:8989)
> **NOTE:** I built the Docker image in the repo on my MacBook with an M2 chip. If you need to run it on a different architecture, you'll have to <a href="https://docs.docker.com/engine/reference/commandline/build/" target="_blank">build it</a> on your desired system.
