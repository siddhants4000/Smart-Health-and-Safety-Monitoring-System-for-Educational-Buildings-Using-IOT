(define (domain smart-building)
  (:requirements :strips :typing)
  
  (:predicates
    (dark)
    (motion-detected)
    (sound-detected)
    (led-on)
    (buzzer-on)
  )

  (:action activate-safety-motion
    :parameters ()
    :precondition (and dark motion-detected)
    :effect (and (led-on) (buzzer-on))
  )

  (:action activate-safety-sound
    :parameters ()
    :precondition (and dark sound-detected)
    :effect (and (led-on) (buzzer-on))
  )
)
