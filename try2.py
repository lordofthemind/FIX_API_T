import quickfix as fix
import logging
import random
import time

# Global Configuration
username = "your_username"
password = "your_password"
target_id = "TARGET"
sender_id = "SENDER"
currency_pairs = ["EUR/USD", "USD/JPY", "GBP/USD"]

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", filename="fix_messages.log"
)


class Application(fix.Application):
    def onCreate(self, sessionID):
        self.sessionID = sessionID
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        logging.info(f"Logon: {sessionID}")

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type == fix.MsgType_Logon:
            message.setField(fix.Username(username))
            message.setField(fix.Password(password))
        logging.info(f"Sent to admin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"Received from admin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"Sent to app: {message}")

    def fromApp(self, message, sessionID):
        logging.info(f"Received from app: {message}")


def send_heartbeat(sessionID):
    heartbeat = fix.Message()
    heartbeat.getHeader().setField(fix.MsgType(fix.MsgType_Heartbeat))
    fix.Session.sendToTarget(heartbeat, sessionID)


def send_logon(sessionID):
    logon = fix.Message()
    logon.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
    logon.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
    logon.setField(fix.EncryptMethod(0))
    logon.setField(fix.HeartBtInt(30))
    fix.Session.sendToTarget(logon, sessionID)


def send_market_data_request(
    sessionID,
    subscription_type=fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES,
    depth=1,
):
    req = fix.Message()
    req.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
    req.setField(fix.MDReqID("12345"))
    req.setField(fix.SubscriptionRequestType(subscription_type))
    req.setField(fix.MarketDepth(depth))
    symbol = random.choice(currency_pairs)
    group = fix.Group(fix.NoRelatedSym(), fix.Symbol())
    group.setField(fix.Symbol(symbol))
    req.addGroup(group)
    fix.Session.sendToTarget(req, sessionID)


def send_new_order_single(sessionID, order_type, time_in_force, quantity, price=None):
    order = fix.Message()
    order.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    order.setField(fix.ClOrdID(str(random.randint(1000, 9999))))
    order.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
    order.setField(fix.Symbol(random.choice(currency_pairs)))
    order.setField(fix.Side(fix.Side_BUY))  # or fix.Side_SELL
    order.setField(fix.TransactTime())
    order.setField(fix.OrdType(order_type))
    if order_type == fix.OrdType_LIMIT:
        order.setField(fix.Price(price))
    order.setField(fix.OrderQty(quantity))
    order.setField(fix.TimeInForce(time_in_force))
    fix.Session.sendToTarget(order, sessionID)


def send_order_cancel_request(sessionID, cl_ord_id, orig_cl_ord_id, symbol):
    cancel_req = fix.Message()
    cancel_req.getHeader().setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
    cancel_req.setField(fix.ClOrdID(cl_ord_id))
    cancel_req.setField(fix.OrigClOrdID(orig_cl_ord_id))
    cancel_req.setField(fix.Symbol(symbol))
    cancel_req.setField(fix.Side(fix.Side_BUY))  # or fix.Side_SELL
    cancel_req.setField(fix.TransactTime())
    fix.Session.sendToTarget(cancel_req, sessionID)


def send_order_status_request(sessionID, cl_ord_id, symbol):
    status_req = fix.Message()
    status_req.getHeader().setField(fix.MsgType(fix.MsgType_OrderStatusRequest))
    status_req.setField(fix.ClOrdID(cl_ord_id))
    status_req.setField(fix.Symbol(symbol))
    fix.Session.sendToTarget(status_req, sessionID)


def main():
    settings = fix.SessionSettings("config.cfg")
    application = Application()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
    initiator.start()

    while True:
        if application.sessionID:
            send_heartbeat(application.sessionID)
            send_market_data_request(application.sessionID)
        time.sleep(30)  # Adjust as needed


if __name__ == "__main__":
    main()
