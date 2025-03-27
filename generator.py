from flask import Flask, request, jsonify, render_template
import stripe
import os

app = Flask(__name__)

# Clé secrète Stripe (remplacez par la vôtre)
stripe.api_key = 'sk_test_51R3L0vQb63B1zRMdXN2RJWISlT8zXGq1hdk2iqDHFEeaskPsKurqK0oMeBzqfgInIkFO4kXxcSFXOYEeWL8i2dwe00tyDddPTG'


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Création de site web',
                    },
                    'unit_amount': 30000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/success')
def success():
    return "Paiement réussi ! Votre site est en cours de création..."


@app.route('/generate-site', methods=['POST'])
def generate_site():
    site_type = request.json.get('type', 'default')
    site_content = f"""<!DOCTYPE html>
    <html lang='fr'>
    <head><meta charset='UTF-8'><title>Votre {site_type}</title></head>
    <body><h1>Bienvenue sur votre {site_type} !</h1></body>
    </html>"""

    site_path = f'sites/{site_type}.html'
    os.makedirs('sites', exist_ok=True)
    with open(site_path, 'w', encoding='utf-8') as file:
        file.write(site_content)

    return jsonify({'message': 'Site généré avec succès !', 'url': f'/{site_path}'})


if __name__ == '__main__':
    app.run(debug=True)
