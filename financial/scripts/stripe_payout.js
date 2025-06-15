const Stripe = require('stripe');
require('dotenv/config');

const stripe = new Stripe(process.env.STRIPE_KEY);

module.exports = async function () {
  try {
    const balance = await stripe.balance.retrieve();
    const availableFunds = balance.available[0]?.amount || 0;

    // Minimum payout threshold: $1,000
    if (availableFunds < 100000) {
      console.log('🔒 Payout threshold not met:', availableFunds / 100);
      return;
    }

    await stripe.transfers.create({
      amount: availableFunds,
      currency: 'usd',
      destination: process.env.MAIN_PAYOUT_ACC,
      description: 'Automated daily payout by GhostFlow AI',
    });

    console.log('✅ Payout successfully sent:', availableFunds / 100);
  } catch (error) {
    console.error('❌ Stripe payout failed:', error);
  }
};
