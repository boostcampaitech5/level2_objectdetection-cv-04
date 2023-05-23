checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=500,
    hooks=[
        dict(type="TextLoggerHook", interval=500),
        dict(
            type="WandbLoggerHook",
            interval=1000,
            init_kwargs=dict(
                project="Recycle Project",
                entity="level1-cv19",
                name="실험할때마다 RUN에 찍히는 이름",  # TODO name을 실험때마다 바꾸어 줘야함
            ),
        ),
    ],
)
# yapf:enable
custom_hooks = [dict(type="NumClassCheckHook")]

dist_params = dict(backend="nccl")
log_level = "INFO"
load_from = None
resume_from = None
workflow = [("train", 1)]  # [('train', 5), ('val', 1)] 이러면 검증을 매 5에폭마다 수행할 수 있음

# disable opencv multithreading to avoid system being overloaded
opencv_num_threads = 0
# set multi-process start method as `fork` to speed up the training
# mp_start_method = 'fork'

# Default setting for scaling LR automatically
#   - `enable` means enable scaling LR automatically
#       or not by default.
#   - `base_batch_size` = (8 GPUs) x (2 samples per GPU).
auto_scale_lr = dict(enable=False, base_batch_size=16)
