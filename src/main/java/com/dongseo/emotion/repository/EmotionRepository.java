package com.dongseo.emotion.repository;

import com.dongseo.emotion.entity.Emotion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EmotionRepository extends JpaRepository<Emotion, Long> {
    public List<Emotion> findAllByUser(String user);
}
