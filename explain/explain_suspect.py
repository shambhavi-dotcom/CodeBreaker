def explain_wallet(wallet_id, G, risk_scores, features_df, illicit_wallets):
    """
    Returns human-readable reasons why a wallet is suspicious
    """

    explanation = []

    # Rule-based explanations
    if wallet_id in illicit_wallets:
        explanation.append("Directly identified as an illicit wallet")

    if features_df.loc[wallet_id, "out_degree"] > 10:
        explanation.append("High fan-out behavior (many outgoing transactions)")

    if features_df.loc[wallet_id, "in_degree"] > 10:
        explanation.append("High fan-in behavior (many incoming transactions)")

    if features_df.loc[wallet_id, "pagerank"] > 0.05:
        explanation.append("Highly central wallet in the transaction network")

    if risk_scores.get(wallet_id, 0) > 0.7:
        explanation.append("High heuristic risk score based on rule-based analysis")

    return explanation
