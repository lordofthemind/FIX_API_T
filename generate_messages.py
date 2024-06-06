import quickfix as fix


def create_market_data_request_reject(mdReqID, reason):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_MarketDataRequestReject))
    message.setField(fix.MDReqID(mdReqID))
    message.setField(fix.Text(reason))
    return message


def create_market_data_snapshot_full_refresh(mdReqID, symbol, marketData):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_MarketDataSnapshotFullRefresh))
    message.setField(fix.MDReqID(mdReqID))
    message.setField(fix.Symbol(symbol))
    for data in marketData:
        group = fix.Group(268, 269)
        group.setField(fix.MDEntryType(data["MDEntryType"]))
        group.setField(fix.MDEntryPx(data["MDEntryPx"]))
        group.setField(fix.MDEntrySize(data["MDEntrySize"]))
        message.addGroup(group)
    return message


def create_new_order_single(clOrdID, symbol, side, orderQty, price, timeInForce):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    message.setField(fix.ClOrdID(clOrdID))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.OrderQty(orderQty))
    message.setField(fix.Price(price))
    message.setField(fix.TimeInForce(timeInForce))
    return message


def create_order_cancel_request(origClOrdID, clOrdID, symbol, side):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
    message.setField(fix.OrigClOrdID(origClOrdID))
    message.setField(fix.ClOrdID(clOrdID))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    return message


def create_execution_report(
    orderID, execID, execType, ordStatus, symbol, side, leavesQty, cumQty, avgPx
):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
    message.setField(fix.OrderID(orderID))
    message.setField(fix.ExecID(execID))
    message.setField(fix.ExecType(execType))
    message.setField(fix.OrdStatus(ordStatus))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.LeavesQty(leavesQty))
    message.setField(fix.CumQty(cumQty))
    message.setField(fix.AvgPx(avgPx))
    return message
