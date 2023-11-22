import stripe

# Set your secret key
stripe.api_key = "sk_test_51O9FyrErLa42fbUSMRlT5TYaoYnro6Gsq7mq2iSmHKMj2kU2G9pzkz61PHFQANQdvJN471f46VyydY6abf6SRmNV00oadLxKEw"

def cancel_payment(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        cancelled_payment_intent = payment_intent.cancel()
        print(f"PaymentIntent {cancelled_payment_intent.id} has been canceled.")

    except Exception as e:
        print(str(e))


def refund_payment(payment_intent_id):
    try:
        # Retrieve the PaymentIntent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Check if the PaymentIntent is refundable
        if payment_intent['status'] == 'succeeded':
            # Create a refund
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id
            )

            print(f"Refund successful. Refund ID: {refund['id']}")
        else:
            print("PaymentIntent is not in a refundable state.")

    except stripe.error.StripeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    payment_intent_id = "pi_3OEo6ZErLa42fbUS0Ijdj8cT_secret_QT8epbBiHzDz89OV2b3wzfH7Z"
    p = payment_intent_id.split("_secret")
    refund_payment(p[0])




