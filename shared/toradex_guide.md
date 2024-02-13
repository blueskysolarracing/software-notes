# Toradex Guide for BFM Development
This guide should give a summarized overview of how to work with the Toradex 
board used to control the BSSR BFM.

It is recommended to use a unix environment to interact with the Toradex board
and to do any developmment on it since Toradex uses a Linux-based OS.
For windows, this means installing a vm, wsl, or dual booting.

Listed below are a few useful resources:
1. Device Tree Overlays used for configuring pins: https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon/
2. Device Tree as an alternative for pin configuration for more control: https://developer.toradex.com/software/linux-resources/device-tree/first-steps-with-device-trees/
2. Insalling WSL on Windows: https://learn.microsoft.com/en-us/windows/wsl/install
3. Apalis Module Datasheet: https://docs.toradex.com/105526-apalis-imx8-datasheet.pdf
4. Ixora Development Board Datasheet: https://docs.toradex.com/101430-apalis-arm-ixora-datasheet.pdf

## Connecting to the board over SSH
* The board is interacted with using ssh
* This means you need to connect the board to the shop wifi using ethernet or 
    an antenna
* First, you should join the BSSR wifi on your computer
* Connect to the board by using the command to torizon@apalis-imx8-07107494
    * Note that "torizon" is the board username and "apalis-..." is the hostname

## Testing and Running code on the board
From this point, it will be assumed that you have ssh'd into the board

### Docker Speedrun
Toradex uses Docker to organize programs on the board. If you are not familiar
with Docker, it basically allows you to create a bunch of virtual computers 
called containers in Docker lingo on a device  so you could install different operating systems, 
programs, and libraries on each of these virtual computers. They are all 
running on the same hardware though. On the Toradex board, you can run the 
command "docker" in the terminal to see a list of available options. A basic 
command you can run is docker ps -a which displays a list of all the running 
and stopped virtual computers (AKA containers).

### Running code
This is one way to test and debug code on the Toradex code.

A testing container called "romantic_bouman" was created using docker commands.

1. ssh into the board
2. Run the command "docker ps -a" and ensure that romantic_bouman is listed
3. Run the command "docker start romantic_bouman"
4. To gain access to the conainer's terminal run "docker exec -it romantic_bouman bash"
5. Now your shell should change. You are ssh'd into the toradex board and now you have just
accessed a virtual computer running on the board.
6. Run the command "cd ~" to enter to the home directory where you should see
a few python scripts in the directory "torizon_tests"
7. Run "python name_of_script.py" to run test code
8. You can use a text editor installed in the container to quickly edit code such as
nano, vim, or nvim which can be installed using terminal commands.

# Editing Pinout Configuration on BFM
The Toradex itself comes with its own pinout configuration already applied, meant for one of the development boards that you can buy from their website.

However, should you not want to be wire constrained when designing a PCB for a toradex module running through, say, a SODIMM slot, you may want to know how to edit the pinout configuration to your custom preference.

## The Premise
Custom pinout configurations effectively mask a pinout configuration file over the default pinout configuration (Device Tree Overlay -> Device Tree -> Torizon OS).
The “Device Tree” refers to the lookup table of pins being configured to GPIO, I2C, SPI, etc.

The overlay simply changes a few of those default pins, then it's **masked** over the default device tree, then the OS executes instructions and sends data out the configured pins accordingly (or receives data).


## Configuring pins (Device Tree Overlays)
In the link https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon/#approach-1-applying-device-tree-overlays-to-an-image-using-a-single-torizoncore-builder-command
follow the steps to be able to compile and upload a device tree overlay. Device Tree Overlays (DTOs) are used to modify what pins on the board do what (Ex: GPIO, AN_ADC, SPI, ...).
Below is a condensed version of this guide.

### Checking for Torizon Core Builder
Torizon Core builder is Toradex’s own firmware tool (terminal command) to make changes and “build” the chip for your purposes. 

First you need to understand the BFM debugging setup:

- The SSH connects directly to the board
- Torizon Core is installed and edited on your OWN machine, or on any server that might have remote access to the BFM
- To install Torizon Core Builder, you need to first install windows linux subsystem, WSL.
  - [How to Install WSL](https://www.notion.so/How-to-Install-WSL-03083e3332fb462b8d6c5398cad48e4a?pvs=21)
    
- After installing WSL you should be able to install Torizon Core Builder **inside** the WSL by following the following commands
    - `mkdir -p ~/tcbdir/ && cd ~/tcbdir/`
        - creates a directory
    - `wget https://raw.githubusercontent.com/toradex/tcb-env-setup/master/tcb-env-setup.sh`
        - grabs the source code
    - `source tcb-env-setup.sh`
        - build the source
- You can then check that it’s properly installed by running and seeing no errors
    - `torizoncore-builder --help`
- If you would like to install docker, you can follow the commands here
    - [Installing Docker on Windows via WSL - Dataedo Documentation](https://dataedo.com/docs/installing-docker-on-windows-via-wsl)

### Editing the Device Tree
If you are using Windows then use the WSL terminal. If you are using Mac or Linux, just use the regular terminal.

1. First enter WSL
2. Then enter docker by typing `sudo systemctl start docker` you can test it has started by typing `docker run --rm hello-world`
    1. There are some known issues where a previous exit code error prevents docker from starting in the next instance.
[How to Fix control process exited with error code.](https://www.notion.so/How-to-Fix-control-process-exited-with-error-code-58f8e90e803e436da9dba986e18a1727?pvs=21)
1. Then start the `tcb-env-setup.sh`, start `torizoncore-builder -h` 
2. Install dependencies and packages
    1. To get the files that correspond to the current board, we need to execute the following with the toradex connected to the bssr network (ie. plug in an ethernet cable) and your computer connected to the bssr wifi.
        ```bash
        # 10.0.1.53 is the board local IP address
        torizoncore-builder images download --remote-host 10.0.1.53 --remote-username torizon --remote-password bssr
        # Wait a while ...
        torizoncore-builder dt checkout
        ```
        
    2. This should create a directory in tcbdir called device-trees
    3. The device trees should be in the directory tcbdir/device-trees/dts-arm64/
    4. You can copy an existing device tree to a new .dts file in this directory and add any changes
    5. You can find how to mux pins by looking in device-trees/include/dt-bindings/pinctrl/pads-imx8qm.h and referencing the datasheet https://docs.toradex.com/105526-apalis-imx8-datasheet.pdf. Muxing pins changes the original functionality to an ALTX pin as specified in the datasheet.
    
3. Push changes to the board by running the commands
```bash
torizoncore-builder dt apply device-trees/dts-arm64/bssr.dts
torizoncore-builder union custom-branch
torizoncore-builder deploy custom-branch --remote-host 10.0.1.53 --remote-username torizon --remote-password bssr --reboot
```

To actually create your own overlay, you can create a new file in the overlays directory that is inspired by some of the other overlays.
When configuring pins that have multiple functionality (what the docs calls pin multiplexing) the current board uses constant definitions located in the following directory:
 ```
tcbdir/device-trees/include/dt-bindings/pinctrl/pads-imx8qm.h
 ```

An example device tree overlay is seen below where <IMX8QM_USDHC2_DATA2_LSIO_GPIO5_IO28 0x104>
configures the USDHC2_DATA2 pin to be GPIO5_IO28.

```
/dts-v1/;
/plugin/;

#include <dt-bindings/pinctrl/pads-imx8qm.h>

/ {
    compatible = "toradex,apalis-imx8";
};
&iomuxc {
       pinctrl-names = "default";
        pinctrl-0 = <&test_regen>;


        apalis-imx8qm {
                test_regen: gpiogrp {
                        fsl,pins =
                                <IMX8QM_USDHC2_DATA2_LSIO_GPIO5_IO28 0x104>;
                };
        };
};
```

### More control with Device Trees
Sometimes Device Tree Overlays do not give you enough control.
In this case you maight have to modify the Device Tree.

After following the "Configuring Pins" section:
1. Make a copy of the Device Tree being used which is imx8qp-apalis-v1.1-ixora-v1.1.dts
2. This has a few includes of other .dtsi files that specify the actual peripherals
3. You can then apply this copied and edited device tree using:
```bash
torizoncore-builder dt apply device-trees/dts-arm64/bssr.dts
torizoncore-builder union custom-branch
torizoncore-builder deploy custom-branch --remote-host 10.0.1.53 --remote-username torizon --remote-password bssr --reboot
```
5. An example bssr.dts file is shown:s

 ```C
    // SPDX-License-Identifier: GPL-2.0+ OR X11
    /*
     * Copyright 2019-2020 Toradex
     */
    
    /dts-v1/;
    
    #include "imx8qm-apalis-v1.1.dtsi"
    #include "imx8-apalis-ixora-v1.1.dtsi"
    
    / {
            model = "Toradex Apalis iMX8QM V1.1 on Apalis Ixora V1.1 Carrier Board";
            compatible = "toradex,apalis-imx8-v1.1-ixora-v1.1",
                         "toradex,apalis-imx8-v1.1-ixora",
                         "toradex,apalis-imx8-v1.1",
                         "toradex,apalis-imx8",
                         "fsl,imx8qm";
    };
    
    // Pin muxing group
    &iomuxc {
           pinctrl-names = "default";
            pinctrl-0 = <&pinctrl_bssr>;
    
            apalis-imx8qm {
                    pinctrl_bssr: bssrgpiogrp {
    												                            // Changes one pin to function as another
                            fsl,pins =
                                    <IMX8QM_USDHC2_DATA2_LSIO_GPIO5_IO28 0x104>,
                                    <IMX8QM_LVDS1_I2C1_SDA_LSIO_GPIO1_IO15 0x104>,
                                    <IMX8QM_ENET1_MDIO_LSIO_GPIO4_IO17 0x104>,
                                    <IMX8QM_ADC_IN5_LSIO_GPIO3_IO23 0x104>,
                                    <IMX8QM_ADC_IN6_LSIO_GPIO3_IO24 0x104>,
                                    <IMX8QM_ADC_IN7_LSIO_GPIO3_IO25 0x104>,
                                    <IMX8QM_SPI0_CS0_LSIO_GPIO3_IO05 0x104>,
                                    <IMX8QM_ESAI0_TX4_RX1_LSIO_GPIO2_IO30 0x104>,
                                    <IMX8QM_ESAI0_TX5_RX0_LSIO_GPIO2_IO31 0x104>,
    
                                    // Misc Module
                                    <IMX8QM_GPT0_COMPARE_LSIO_GPIO0_IO16 0x104>, // left indicator
                                    <IMX8QM_UART0_RTS_B_LSIO_GPIO0_IO22 0x104>, // right indictor
                                    <IMX8QM_UART0_CTS_B_LSIO_GPIO0_IO23 0x104>, // brake light
                                    <IMX8QM_GPT1_COMPARE_LSIO_GPIO0_IO19 0x104>, // DRL
                                    <IMX8QM_ENET1_RGMII_TXD3_LSIO_GPIO6_IO15 0x104>, // Horn
                                    <IMX8QM_ESAI1_SCKT_LSIO_GPIO2_IO07 0x104>, // Driver Fan
                                    <IMX8QM_ENET1_REFCLK_125M_25M_LSIO_GPIO4_IO16 0x104>, // Backup camera
    																
    																// Relay Module
                                    <IMX8QM_ENET1_RGMII_RXD0_LSIO_GPIO6_IO18 0x104>,// Array High Side Relay
                                    <IMX8QM_ENET1_RGMII_TXD2_LSIO_GPIO6_IO14 0x104>, // Array Low Side Relay
                                    <IMX8QM_ENET1_RGMII_TXD1_LSIO_GPIO6_IO13 0x104>,// Array Precharge Relay
                                    <IMX8QM_ENET1_RGMII_RXD3_LSIO_GPIO6_IO21 0x104>,// Battery High Side Relay
                                    <IMX8QM_ENET1_RGMII_RXD2_LSIO_GPIO6_IO20 0x104>, // Battery Low Side Relay
                                    <IMX8QM_ENET1_RGMII_RXD1_LSIO_GPIO6_IO19 0x104>, // Battery Precharge Relay
                                    <IMX8QM_FLEXCAN2_TX_LSIO_GPIO4_IO02 0x104>,// Module Fan
                                    //<>,// Intake Fan
                                    //<>,// Vent Fan
    
                                    <IMX8QM_ENET1_MDC_LSIO_GPIO4_IO18 0x104>, // Safe state trigger
                                    <IMX8QM_LVDS0_GPIO00_LSIO_GPIO1_IO04 0x104>, // 12V_Source_Asc_Switch
                                    <IMX8QM_MIPI_DSI1_GPIO0_00_LSIO_GPIO1_IO22 0x104>, // MPPT_ON
                                    <IMX8QM_QSPI1A_DQS_LSIO_GPIO4_IO22 0x104>, // BMS_COMMS_STATUS_LED
    
                                    <IMX8QM_USDHC2_CMD_LSIO_GPIO5_IO25 0x104>, // Spare 0
                                    <IMX8QM_FLEXCAN1_TX_LSIO_GPIO4_IO00 0x104>, // Spare 2
    
                                    <IMX8QM_USB_SS3_TC3_LSIO_GPIO4_IO06 0x104>; // LED0
                    };
    
                    pinctrl_bssr_lpspi0: bssrlpspi0grp {
                            fsl,pins = <
                                    IMX8QM_SPI0_SCK_DMA_SPI0_SCK                    0x0600004c
                                    IMX8QM_SPI0_SDO_DMA_SPI0_SDO                    0x0600004c
                                    IMX8QM_SPI0_SDI_DMA_SPI0_SDI                    0x0600004c
                            >;
                    };

                    // For motor pots
                    pinctrl_bssr_lpspi3: bssrlpspi3grp {
                    fsl,pins = <
                            IMX8QM_UART1_TX_DMA_SPI3_SCK                    0x0600004c
                            IMX8QM_UART1_RX_DMA_SPI3_SDO                    0x0600004c
                            IMX8QM_UART1_RTS_B_DMA_SPI3_SDI                 0x0600004c
                        >;
                    };
    
                    pinctrl_bssr_uart: bssruartgrp {
                            fsl,pins =
                                    <IMX8QM_LVDS0_I2C1_SCL_DMA_UART2_TX 0x104>, // Radio Tx
                                    <IMX8QM_LVDS0_I2C1_SDA_DMA_UART2_RX 0x104>; // Radio Rx
                    };
            };
    };
    
    // The below changes spi to not have a chip select
    
    /delete-node/ &pinctrl_lpspi0;
    
    &lpspi0 {
            pinctrl-names = "default";
            pinctrl-0 = <&pinctrl_bssr_lpspi0>;
            #address-cells = <1>;
            #size-cells = <0>;
            /delete-property/ cs-gpios;
    
            spidev0: spi@0 {
                    compatible = "toradex,evalspi";
                    reg = <0>;
                    spi-max-frequency = <4000000>;
            };
    };
    ```
