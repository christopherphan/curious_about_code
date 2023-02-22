(; Solution to to David Amos's Weekly Coding Challenge:
 ; https://discourse.davidamos.dev/t/adding-it-all-up/139
 ;)

(module

  (func $triang
    ;; Return the nth triangular number
    ;; Computes from scratch rather than using n * (n + 1) / 2 formula
    (param $n i64)
    (result i64)
    (local $k i64) ;; iterator
    (local $r i64) ;; result
    i64.const 1
    local.set $k ;; k = 1
    i64.const 0
    local.set $r ;; r = 0
    (loop $main ;; while k <= n
        local.get $k
        local.get $r
        i64.add
        local.set $r ;; r = k + r
        i64.const 1
        local.get $k
        i64.add
        local.tee $k ;; k = k + 1
                     ;; store in k and put back on stack
        local.get $n
        i64.le_u
    br_if $main)
    local.get $r ;; return r
  )

  (func $f
    ;; The desired function
    (export "ourfunc")
    (param $n i64)
    (result i64)
    (local $r i64) ;; result
    local.get $n
    i64.const 0
    i64.gt_s
    (if $pos_exec ;; if n > 0
      (then
        local.get $n
        call $triang
        local.set $r ;; r = triang(n)
      )
      (else
        local.get $n
        i64.const 0
        i64.eq
          (if $zero_exec ;; if n == 0
            (then
              i64.const 0
              local.set $r ;; r = 0
            )
            (else
              i64.const 0
              local.get $n
              i64.sub
              local.tee $n ;; n = -1 * n
                           ;; store in n and put back on stack
              call $triang
              i64.const 0
              i64.sub
              local.set $r ;; r = -1 * triang(n)
            )
          )
        )
      )
    local.get $r
  ) ;; return r
)
