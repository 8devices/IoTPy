
What is IoTPy?
==============

IoTPy is a Python library which provides an easy way to interface and control electronic systems.
It consists of three main parts:

1. **Core**

   IoTPy core is a set of abstract classes (a.k.a *core* components). Each class represents a generic electronic module,
   interface or capability (such as GPIO, ADC, SPI, etc.) and describes what functionality should it have. These classes
   usually have no actual code and are only descriptive: for IoTPy users it's a reference as to what expect from
   system-specific implementations and for developers (implementers) it's a description how should their code behave.

2. **Platforms**

   This is system-specific implementations of the *core* components. Platforms can take many forms: they can be generic
   (like Linux) or specific to a certain board (like UPER1) or even a mixture of the two, like the Carambola2 board,
   which uses some of the Linux components, while also maintaining a part of Carambola2-only code. However there are
   some implementation guidelines:

   * Platforms are NOT required to implement ALL *core* components.
   * Platforms are NOT required to implement ALL functions of a specific *core* component, but in that case, calling such function(s) should throw NotImplementedError (default action if `core` class is inherited).
   * Platform components CAN have more functionality than the equivalent *core* component.
   * It is RECOMMENDED that the platform component, would inherit *core* component.
   * Most importantly, for all implemented functions MUST behave EXACTLY like described by *core* component.

3. **Things**

   Things is a collection of system-independent electronic gadgets, that (usually) use a certain *core* component to
   establish a more specific functionality. For example, a lot of the "things" are sensors (like LM75), that use *core*
   communication interface (i.e. I2C) and allow you to measure temperature, humidity, pressure, etc. But, of course,
   there are other type of *things* like rotary encoders, stepper motors, flash memory controllers.
