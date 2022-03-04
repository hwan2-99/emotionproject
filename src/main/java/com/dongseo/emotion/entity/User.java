package com.dongseo.emotion.entity;

import lombok.*;

import javax.persistence.Entity;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    private String id;
    private String pw;
}
