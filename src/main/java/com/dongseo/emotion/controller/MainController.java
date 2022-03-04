package com.dongseo.emotion.controller;

import com.dongseo.emotion.entity.Emotion;
import com.dongseo.emotion.entity.User;
import com.dongseo.emotion.service.EmotionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.List;

@Slf4j
@Controller
@RequiredArgsConstructor
@RequestMapping("/v1")
public class MainController {

    private final EmotionService emotionService;
    @GetMapping("login")
    public String loginPage( HttpSession session, Model model){

        model.addAttribute("user","a");
        return "login";
    }
    @PostMapping("login")
    public String login( User user, HttpSession session){

        if(user.getId().equals("admin") && user.getPw().equals("a")){
            session.setAttribute("user", "admin");
            return "redirect:/v1/emotion/user";
        }else{
            return "redirect:/v1/login";
        }
    }
    @GetMapping("logout")
    public String logout(HttpSession session){

        session.removeAttribute("user");
        return "redirect:/v1/login";
    }
    @GetMapping("emotion/user")
    public String userEmotion(HttpSession session, Model model){
        if(session.getAttribute("user")==null){
            return "login";
        }
        log.info((String)session.getAttribute("user"));
        log.info(emotionService.userEmotionService((String)session.getAttribute("user")).toString());
        model.addAttribute("result", emotionService.userEmotionService((String)session.getAttribute("user")));
        model.addAttribute("user", (String)session.getAttribute("user"));
        return "userEmotion";
    }

    @GetMapping("emotion/user/{method}")
    public String userEmotionDetail(@PathVariable String method, HttpSession session, Model model){
        if(session.getAttribute("user")==null){
            return "login";
        }
        model.addAttribute("result", emotionService.emotionDetailService((String)session.getAttribute("user"), method));
        model.addAttribute("user", (String)session.getAttribute("user"));
        return "userEmotion"+method;
    }
}
