<div id="top"></div>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/g-tejas/ChainNet">
    <img src="images/chainnet.png" alt="Logo">
  </a>

  <p align="center">
    A macro risk oscillator metric to give you a better sensing of the current state of the market.
    <br />
    <a href="http://chainnet.herokuapp.com/"><strong>Explore web app »</strong></a>
    <br />
    <br />
    <a href="https://github.com/g-tejas/ChainNet/issues">Report Bug</a>
    ·
    <a href="https://github.com/g-tejas/ChainNet/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
"One of the exciting prospects in on-chain analysis is the ability to to visualize the tectonic forces of underlying
supply & demand governing the Bitcoin market. For the first time in finance, we can observe the near real-time transfer of an
asset from stronger to weaker hands in a bull run, the accumulation by long-term investors in a bear market, and the fluctuating
profit-and-loss of entities day to day.

The data is public, but the interpretation is nuanced.

With this newfound transparency is the symbiotic relationship between long- and short-term investors- a perpetual tug-of-war between
high and low time prefrences that characterizes unique phases of market cycles. By tracking the movement of supply between
these two groups, we gain measurable insights that show us when macros trend shifts are underway." ~ [Glassnode Insights](https://insights.glassnode.com/follow-the-smart-money/)

Chain Net is built on a risk oscillator metric which aggregates multiple on-chain and price data, and is normalized into [0, 1] range. 0 being very low risk and 1 being extremely high risk. It gives a rough gauge of how far Bitcoin is from it's market cycle peak and bottom. 

Currently, the metrics involved are,
  
| Metric | Included in final calculation | Build status |
|--------|:-------------:|:---:|
| Mayer Multiple | ✅ | ✅ |
|Puell Multiple | ✅ | ✅ |
|Price/52W EMA | ✅ | ✅ |
|Sharpe Ratio | ✅ | ✅ |
|Sortino Ratio  | ❌ | ✅ |
|Power Law  | ✅ | ✅ |
|400D MA| ✅ | ✅ |
| Supply Delta| ❌ | ❌ |




The risk metric is then used in a trading strategy, which is a work in progress. We will post
the results soon. 

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* [Quandl API](https://www.quandl.com)
* Pandas & Numpy
* Plotly

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Telegram Bot 
  - [] Provide Hourly/Daily/Weekly notifications on risk levels
- [] For runnning the code locally, include pyfiglet to display risk level when started up. 
- [] Include on-chain metrics in the model 
    - [] [Supply Delta](https://medium.com/capriole/a-simple-metric-to-identify-bitcoin-tops-999232e96dc0)
    - [] Stock-to-flow model?
- [] Connect to FTX to place trades?

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b g-tejas/ChainNet`)
3. Commit your Changes (`git commit -m 'Added new feature'`)
4. Push to the Branch (`git push origin g-tejas/ChainNet`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

[Tejas Garrepally](gtejas.com) - ttejasgarrepally@gmail.com

Project Link: [g-tejas/ChainNet](https://github.com/g-tejas/ChainNet)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Bitcoin Raven](https://www.youtube.com/channel/UCrlkqSLmHL8ZPVpOxj7La4Q/about)
* [Claude Fars](https://github.com/ClaudeF4491)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/g-tejas/ChainNet.svg?style=for-the-badge
[contributors-url]: https://github.com/g-tejas/ChainNet/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/g-tejas/ChainNet.svg?style=for-the-badge
[issues-url]: https://github.com/g-tejas/ChainNet/issues
[license-shield]: https://img.shields.io/github/license/g-tejas/ChainNet.svg?style=for-the-badge
[license-url]: https://github.com/g-tejas/ChainNet/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
