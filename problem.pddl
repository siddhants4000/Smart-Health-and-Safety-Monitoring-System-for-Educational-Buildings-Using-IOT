(define (problem building-scenario)
  (:domain smart-building)
  (:init
    (sound-detected)
    (led-off)
    (buzzer-off)
  )
  (:goal (and (led-on) (buzzer-on)))
)
