import 'package:flutter/material.dart';

Color hexToColor(String hex) {
  hex = hex.replaceAll('#', '');
  return Color(int.parse('FF$hex', radix: 16)); // FF is voor volledige opacity
}