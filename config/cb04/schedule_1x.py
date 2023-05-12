# optimizer
optimizer = dict(
    type="SGD", lr=0.02, momentum=0.9, weight_decay=0.0001
)  ##블로그에선 0.02 -> 0.002로 줄였음
optimizer_config = dict(grad_clip=None)  # TODO grad_clip이란????
# learning policy
lr_config = dict(
    policy="step", warmup="linear", warmup_iters=500, warmup_ratio=0.001, step=[8, 11]
)
runner = dict(type="EpochBasedRunner", max_epochs=12)
