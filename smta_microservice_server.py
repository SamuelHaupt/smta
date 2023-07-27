# flake8: noqa

import zmq


def calculate_investment(collection_sent):
    results = []
    single_share_purchase_price, single_share_sold_price, total_amount_initially_invested = collection_sent

    per_share_gain_or_loss = round(single_share_sold_price - single_share_purchase_price, 3)
    percentage_gain_or_loss = round((per_share_gain_or_loss / single_share_purchase_price) * 100, 3)
    investment_profit_or_loss = round((percentage_gain_or_loss / 100) * total_amount_initially_invested, 3)

    results.append((per_share_gain_or_loss, percentage_gain_or_loss, investment_profit_or_loss))
    return results

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        # Wait for incoming request
        collection_sent = socket.recv_pyobj()
        print(collection_sent)
        # Calculate the results
        results = calculate_investment(collection_sent)

        # Send the results back to the client
        print(results)
        socket.send_pyobj(results)

if __name__ == "__main__":
    main()