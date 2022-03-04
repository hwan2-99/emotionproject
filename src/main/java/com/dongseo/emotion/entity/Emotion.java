package com.dongseo.emotion.entity;

import lombok.*;

import javax.persistence.*;
import java.time.LocalDateTime;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity(name ="result")
public class Emotion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(nullable = false)
    private double face;

    @Column(nullable = false)
    private double voice;

    @Column(nullable = false)
    private double brain;

    @Column(nullable = false, length = 100)
    private String user;

    @Column(nullable = false)
    private LocalDateTime createAt;
}
