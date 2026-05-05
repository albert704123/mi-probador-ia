output = replicate.run(
    "yisol/idm-vton",  # Sin :c8718e02
    input={
        "human_img": persona_url,
        "garm_img": prenda_url,
        "garment_des": "una camisa",
        "is_checked": True
    }
)
