import posix_ipc

print("Test")
# Name der Message Queue
MESSAGE_QUEUE_NAME = "/my_message_queue"

# Erstelle eine Message Queue
mq = posix_ipc.MessageQueue(MESSAGE_QUEUE_NAME, posix_ipc.O_CREAT)

# Sende eine Nachricht über die Message Queue
message_to_send = "Hallo, dies ist eine Testnachricht."
mq.send(message_to_send)

# Empfange eine Nachricht über die Message Queue
message_received, _ = mq.receive()

print("Empfangene Nachricht:", message_received)

# Schließe und lösche die Message Queue
mq.close()
posix_ipc.unlink_message_queue(MESSAGE_QUEUE_NAME)