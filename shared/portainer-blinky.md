# Deploy blinky within Portainer

Below is a description of how to deploy blinky within Portainer. This is helpful for debugging.

**Follow steps on portainer-python**

Follow steps on [Python & Portainer Guide](portainer-python.md) until ``Setup Environment``.

**Setup environment.**

First, decide which GPIO port you want to manipulate. We will then see what gpiochip and line it corresponds to.

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/fdca506c-0745-4f7f-bc34-1fad8eeb3855)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/52722b5f-c7dc-47d1-8cde-833a66947f53)

Commands like 'gpioinfo' and 'grep' can be very helpful. Then, you can manipulate gpio with python-periphery or 'gpioset' command.

**Remember path and line**

In the image above, the path is ``/dev/gpiochip2`` and line is ``9``

**Create blinky image**

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/23d14610-821d-4e4d-9bd5-1aacc7180d82)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/8b272ede-c28d-462b-b233-1f26cf588d32)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/1e67fe29-83da-4c06-9130-271f7fb481e4)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/311337f1-b0b7-4475-8d9c-3d5b69f6fb4c)

**Create container with blinky image**

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/c11a07e9-4843-4103-86fb-e548ce3b7934)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/9aa438b6-7341-45c2-aded-1d149a77eced)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/4e2f8564-e7ac-48e9-bf2a-5a1accfcd2e7)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/78af9b05-36f6-455c-9550-3f11212c64ed)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/00b60e09-70ff-46a5-a2ef-43c5d4f9fcb4)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/377b412c-c476-47c5-a2da-a9bac133091f)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/d8e92e28-358c-41fe-9460-2928e9764d39)

**Check LED**

Now the LED should blink! You may turn off the board and restart it. You should still see it blink after the board boots on.

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/1551302f-5229-42d4-bc74-812c4be08ea6)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/522c86b3-ca22-4793-95c7-d26554184614)

![image](https://github.com/blueskysolarracing/software-notes/assets/27718254/9805f808-3392-4008-9a1f-5a40f0a1fc02)
