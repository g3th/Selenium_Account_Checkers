# Selenium Account Checkers

Just scripts using Selenium to learn more about automation. 

Checks for valid accounts on a variety of services, some using a headless browser which includes a user-agent to prevent detection.

**WARNING:**

Checking too many accounts might result in a 'Too many tries' or similar error, and there will be a cool-down period where login for current IP will be disabled.

Includes simple scripts to split any combo list.

### Requires ###

Selenium webdriver, i.e.:

``` apt-get install chromium-driver ```

``` pip3 install selenium ```

``` pip3 install chromedriver-py ```

### To do ###

- Get rid of try blocks
- Use headless for all services
- Use proper checks to determine if accounts are valid (not try blocks)
- Can't think now...
