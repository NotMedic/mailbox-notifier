### Mailbox Notifier

This repo contains code for a pair of Heltec LoRa32 v2 boards to notify you if your mailbox has been opened.  

Basically:
1. The sender is in an off state.
2. The photocell on the sender sees light, sending a signal to the latching relay to power to ESP32.
3. The ESP32 sends a JSON packet containing the notification and the voltage of the LiPo powering the ESP32
4. The reciever recieves this message, turns on an LED, lights up the screen, and sends an ACK back.
5. The sender receives the ACK and powers down.


It's all crude and rough hacker-quality code and wiring, but it works. 
