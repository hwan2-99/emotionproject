package com.dongseo.emotion.dto;

import com.dongseo.emotion.entity.Emotion;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Column;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.time.LocalDateTime;

@NoArgsConstructor
@Getter
public class EmotionDetailDto {
    private long id;
    private double face;

    private double voice;

    private double brain;

    private String user;

    private LocalDateTime createAt;
    private boolean result;

    public EmotionDetailDto(Emotion emotion, boolean result){
        this.id = emotion.getId();
        this.face = emotion.getFace();
        this.voice = emotion.getVoice();
        this.brain = emotion.getBrain();
        this.user = emotion.getUser();
        this.createAt = emotion.getCreateAt();
        this.result = result;
    }
}
