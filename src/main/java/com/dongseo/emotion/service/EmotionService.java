package com.dongseo.emotion.service;

import com.dongseo.emotion.dto.EmotionDetailDto;
import com.dongseo.emotion.entity.Emotion;
import com.dongseo.emotion.repository.EmotionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmotionService {
    private final EmotionRepository emotionRepository;

    public List<Emotion> userEmotionService(String id){
        return emotionRepository.findAllByUser(id);
    }

    public List<EmotionDetailDto> emotionDetailService(String id, String method){
        List<Emotion> emotions = emotionRepository.findAllByUser(id);
        List<EmotionDetailDto> list = new ArrayList<>();
        for(Emotion emotion : emotions){
            EmotionDetailDto emotionDetailDto = new EmotionDetailDto();
            double face = emotion.getFace();
            double voice = emotion.getVoice();
            double brain = emotion.getBrain();
            if(method.equals("Default")){
                emotionDetailDto = new EmotionDetailDto(emotion,emotionDetailDefault(face,voice,brain));
            }if(method.equals("Fuzzy")){
                emotionDetailDto = new EmotionDetailDto(emotion,emotionDetailFuzzy(face,voice,brain));
            }if(method.equals("Maut")){
                emotionDetailDto = new EmotionDetailDto(emotion,emotionDetailMaut(face,voice,brain));
            }if(method.equals("Graph")){
                emotionDetailDto = new EmotionDetailDto(emotion,false);
            }
            list.add(emotionDetailDto);
        }
        return list;

    }
    private boolean emotionDetailDefault(double face, double voice, double brain){
        int cnt = 0;
        if(face >= 0.5) cnt++;
        if(voice >= 0.5) cnt++;
        if(brain >= 0.5) cnt++;

        if(cnt>2) return true;
        else return false;
    }
    private boolean emotionDetailFuzzy(double face, double voice, double brain){
        if(face >= 0.7 && voice >= 0.7 && brain >= 0.7){
            return true;
        }
        else return false;
    }
    private boolean emotionDetailMaut(double face, double voice, double brain){
        if(face * 0.3 + voice * 0.3 + brain * 0.4 > 0.8){
            return true;
        }
        else return false;
    }
}
