# Alternativa 1: OOTDiffusion (modelo más nuevo y estable)
output = replicate.run(
    "levihsu/ootdiffusion",
    input={
        "model_type": "upper_body",  # opciones: "upper_body", "lower_body", "dresses"
        "garment_image": prenda_url,
        "model_image": persona_url,
        "n_samples": 1,
        "guidance_scale": 2.0
    }
)

# Alternativa 2: Otro IDM-VTON (sin hash)
output = replicate.run(
    "yisol/idm-vton",
    input={
        "human_img": persona_url,
        "garm_img": prenda_url,
        "garment_des": "una prenda",
        "is_checked": False
    }
)

# Alternativa 3: Try-on con stable diffusion
output = replicate.run(
    "lucataco/idm-vton",
    input={
        "human_image": persona_url,
        "garment_image": prenda_url
    }
)
