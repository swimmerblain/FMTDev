# Example Installation

Following this very basic installation steps you can build the example code from scratch and test the qb SoftHand Industry functionalities.

```
mkdir build
cd build
cmake ..
make
make install
```

The example code is stored under the `src` directory (it is called `main.cpp` as usual). The building process generates an executable called `qbsofthand_industry_api_example` in the base directory, that can be run in any terminal.

The example prompt on screen the qb SoftHand Industry information and close (and reopen) it just one time.

Before executing the example code, please be sure to have properly connected and powered the device by following the official qb SoftHand Industry User Guide.

Moreover, you need to be connected to the device through a proper ethernet network. The device default parameters are the followings so please set up your network adapter settings to fit this configuration (you may change the device network parameters later).
* Network IPv4: `192.168.1.110`
* Network Mask: `255.255.255.0`
* Network Gateway: `192.168.1.1`
* Network DHCP: `disabled`

For example, you may give the `192.168.1.100` static IPv4 to your network adapter.

If you find any problem during this simple setup, please fell free to raise a support request at [support@qbrobotics.com](support@qbrobotics.com).

# qb SoftHand Industry API

By exploring the simple example code above, you can understand most of the features available for the user. Moreover, the documentation of the whole library can be found both in the User Guide and in the `include/qbsofthand_industry_api/qbsofthand_industry_api.h` header file.

The C++ shared library (compiled for both 32- and 64-bit systems) can be linked against your own project to include the control capability of the qb SoftHand Industry.

If you need special architecture binaries, please make a dedicated support request at [support@qbrobotics.com](support@qbrobotics.com).