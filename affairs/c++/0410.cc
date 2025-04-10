#include <iostream>

class Animal{
public:
    virtual void speak(){
        std::cout<<"Generic animal sound!"<<std::endl;
    }
};

class Dog:public Animal{
public:
    void speak() override{
        std::cout<<"Woof!"<<std::endl;
    }
};

void make_animal_speak(Animal* animal){
    animal->speak();
}

int main(){
    Dog dog;
    make_animal_speak(&dog);
    return 0;
}