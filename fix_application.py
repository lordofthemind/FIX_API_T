import quickfix as fix
import quickfix.Application as Application
import quickfix.Session as Session
import logging
import os
from generate_messages import *
from cred import username, password, sender_comp_id_for_data, target_comp_id

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Username and password
USERNAME = username
PASSWORD = password
SENDER_COMP_ID_FOR_DATA = sender_comp_id_for_data
TARGET_COMP_ID = target_comp_id


# Application class
class FixApp(Application):
    def onCreate(self, sessionID):
        logging.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        logging.info(f"Logon: {sessionID}")

    def onLogout(self, sessionID):
        logging.info(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        if message.getHeader().getField(msgType).getValue() == fix.MsgType_Logon:
            message.setField(fix.Username(USERNAME))
            message.setField(fix.Password(PASSWORD))
        logging.info(f"ToAdmin: {message}")

    def fromAdmin(self, message, sessionID):
        logging.info(f"FromAdmin: {message}")

    def toApp(self, message, sessionID):
        logging.info(f"ToApp: {message}")

    def fromApp(self, message, sessionID):
        logging.info(f"FromApp: {message}")


def send_message(sessionID, message):
    try:
        Session.sendToTarget(message, sessionID)
        logging.info(f"Sent message: {message}")
    except fix.SessionNotFound as e:
        logging.error(f"Session not found: {e}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


def main():
    try:
        settings = fix.SessionSettings("client_market_data2.cfg")
        application = FixApp()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
        initiator.start()

        sessionID = fix.SessionID("FIX.4.4", SENDER_COMP_ID_FOR_DATA, TARGET_COMP_ID)

        # Example usages:

        # 1. Market Data Request Reject
        mdReqReject = create_market_data_request_reject("123", "Invalid Symbol")
        send_message(sessionID, mdReqReject)

        # 2. Market Data Snapshot Full Refresh
        marketData = [
            {
                "MDEntryType": fix.MDEntryType_BID,
                "MDEntryPx": 100.5,
                "MDEntrySize": 200,
            },
            {
                "MDEntryType": fix.MDEntryType_OFFER,
                "MDEntryPx": 101.5,
                "MDEntrySize": 150,
            },
        ]
        mdSnapshot = create_market_data_snapshot_full_refresh("124", "AAPL", marketData)
        send_message(sessionID, mdSnapshot)

        # 3. New Order Single (IOC)
        newOrderIOC = create_new_order_single(
            "125", "AAPL", fix.Side_BUY, 100, 150.0, fix.TimeInForce_IMMEDIATE_OR_CANCEL
        )
        send_message(sessionID, newOrderIOC)

        # 4. New Order Single (FOK)
        newOrderFOK = create_new_order_single(
            "126", "AAPL", fix.Side_BUY, 100, 150.0, fix.TimeInForce_FILL_OR_KILL
        )
        send_message(sessionID, newOrderFOK)

        # 5. Order Cancel Request
        cancelOrder = create_order_cancel_request("125", "127", "AAPL", fix.Side_BUY)
        send_message(sessionID, cancelOrder)

        # 6. Execution Report (Partial Fill)
        execReportPartial = create_execution_report(
            "128",
            "1",
            fix.ExecType_PARTIAL_FILL,
            fix.OrdStatus_PARTIALLY_FILLED,
            "AAPL",
            fix.Side_BUY,
            50,
            50,
            150.0,
        )
        send_message(sessionID, execReportPartial)

        # 7. Execution Report (Full Fill)
        execReportFull = create_execution_report(
            "129",
            "2",
            fix.ExecType_FILL,
            fix.OrdStatus_FILLED,
            "AAPL",
            fix.Side_BUY,
            0,
            100,
            150.0,
        )
        send_message(sessionID, execReportFull)

        # Wait for events or user interaction
        input("Press <Enter> to terminate.")
        initiator.stop()
    except Exception as e:
        logging.error(f"Application error: {e}")


if __name__ == "__main__":
    main()
