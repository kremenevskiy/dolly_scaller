INSERT INTO subscriptions_details (
    subscription_name, subscription_type, cost_rubles, cost_stars, duration,
    is_active, models_count, photos_by_prompt_count, photos_by_image_count
) VALUES
    ('basic',                    'montly',      1000, 10000, 999,     TRUE, 1, 200, 200),
    ('premium',                  'montly',      2000, 20000, 999999,  TRUE, 5, 500, 500),
    ('models_small_pack',        'models',      200,  2000,  NULL,    TRUE, 2, 0, 0),
    ('generations_large_pack',   'generations', 500,  5000,  NULL,    TRUE, 0, 500, 500);