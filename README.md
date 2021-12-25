<div id="top"></div>

<br />
<div align="center">
  <a href="https://github.com/codefair114">
    <img src="https://i.ibb.co/vsnJKbD/1588258.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">EnvYard Embedded</h3>

  <p align="center">
    The embedded code for the EnvYard greenhouse project
    <br />
    <a href="https://youtu.be/YDNRUz6sISo"><strong>View Video »</strong></a>
    <br />
  </p>
</div>



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
      <a href="#installation">Installation</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is an administration app, with multiple sections for the different entities needed to administrate the greenhouse's parcels:
  - Get biometric data from sensors
  - Take images and videos of your greenhouses IRT
  - Adjust environment for the plants on each level
    - Irrigation
    - Ventilation
    - Alerts by email

The presentation of the project is available [here](https://app.slidebean.com/p/mnv80cdywq/EnvYard-Startup).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

The project was built with:

* [Python](https://www.python.org/)
* [Raspberry PI](https://www.raspberrypi.org/)
* [Arduino](https://www.arduino.cc/)
* [Vision API](https://cloud.google.com/vision)
* [MongoDB](https://www.mongodb.com/)

<p align="right">(<a href="#top">back to top</a>)</p>


## Installation

1. Download the repository to your Raspberry Pi

```
$ git clone https://github.com/codefair114/EnvYard-Embedded
```

2. Create virtualenv

```
$ virtualenv venv
```

3. Activate virtualenv

```
$ source venv/bin/activate
```
4. Install libraries
```
$ pip install -r requirements.txt 
```

5. Run script

```
$ ./scripts/setup.sh
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This project can be used as a template for any embedded project.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<p align="right">(<a href="#top">back to top</a>)</p>

